"""
AI Lead Agent - Automated lead generation and client communication agent
"""
from typing import Dict, List, Any
from datetime import datetime
from src.core.logger import log
from src.services.ai.ai_service import AIService
from src.services.discovery.discovery_service import DiscoveryService
from src.services.email.email_service import EmailService


class AILeadAgent:
    """
    AI-powered agent for automated lead generation and client communication.
    Handles the entire workflow from lead discovery to follow-up conversations.
    """

    def __init__(self):
        self.ai_service = AIService()
        self.discovery_service = DiscoveryService()
        self.email_service = EmailService()

    async def generate_leads(
        self,
        industry: str,
        location: str,
        count: int = 10,
        provider_type: str = "mock"
    ) -> List[Dict[str, Any]]:
        """
        Generate qualified leads based on industry and location

        Args:
            industry: Target industry/niche
            location: Target location
            count: Number of leads to generate
            provider_type: Discovery provider to use

        Returns:
            List of generated leads with contact information
        """
        try:
            log.info(f"Starting lead generation for {industry} in {location}")

            # Discover businesses using discovery service
            leads = await self.discovery_service.discover_businesses(
                niche=industry,
                location=location,
                count=count,
                provider_type=provider_type
            )

            # Score and qualify leads
            qualified_leads = []
            for lead in leads:
                # Add lead scoring
                score = await self._score_lead(lead)
                lead['lead_score'] = score
                is_qualified = score > 70
                status = 'qualified' if is_qualified else 'pending'
                lead['qualification_status'] = status
                timestamp = datetime.utcnow().isoformat()
                lead['generated_at'] = timestamp
                qualified_leads.append(lead)

            log.info(f"Generated {len(qualified_leads)} qualified leads")
            return qualified_leads

        except Exception as e:
            log.error(f"Error generating leads: {e}")
            raise

    async def create_personalized_outreach(
        self,
        lead: Dict[str, Any],
        campaign_settings: Dict[str, Any],
        provider_type: str = "mock"
    ) -> Dict[str, str]:
        """
        Create personalized outreach message for a lead

        Args:
            lead: Lead data with business and contact information
            campaign_settings: Campaign configuration (tone, goal, etc.)
            provider_type: AI provider to use

        Returns:
            Generated outreach message with subject and body
        """
        try:
            # Log outreach creation
            business_name = lead.get('business_name', 'Unknown')
            log.info(f"Creating outreach for {business_name}")

            # Prepare lead data for AI
            lead_data = {
                'business_name': lead.get('business_name'),
                'industry': lead.get('industry'),
                'location': lead.get('city'),
                'contact_name': lead.get('contact_name'),
                'contact_email': lead.get('contact_email'),
                'website': lead.get('website'),
                'service_interest': campaign_settings.get('goal')
            }

            # Generate subject line
            subject_prompt = self._create_subject_prompt(
                lead_data,
                campaign_settings.get('tone', 'professional')
            )
            subject = await self.ai_service.classify_intent(subject_prompt)

            # Generate email body directly
            body = await self.ai_service.generate_outreach_content(
                lead_data=lead_data,
                context="email_body",
                provider_type=provider_type
            )

            # Create message object
            default_subject = f"Helping {lead_data['business_name']} Grow"
            message = {
                'lead_id': lead.get('id'),
                'contact_email': lead.get('contact_email'),
                'subject': subject or default_subject,
                'body': body.get('content', ''),
                'tone': campaign_settings.get('tone'),
                'goal': campaign_settings.get('goal'),
                'status': 'draft',
                'created_at': datetime.utcnow().isoformat()
            }

            msg = f"Outreach created for {lead_data['business_name']}"
            log.info(msg)
            return message

        except Exception as e:
            log.error(f"Error creating outreach message: {e}")
            raise

    async def send_outreach_campaign(
        self,
        messages: List[Dict[str, str]],
        auto_followup: bool = True
    ) -> Dict[str, Any]:
        """
        Send outreach messages to multiple leads

        Args:
            messages: List of generated outreach messages
            auto_followup: Whether to enable automatic follow-ups

        Returns:
            Campaign results with sent count and status
        """
        try:
            # Log campaign start
            msg_count = len(messages)
            log.info(f"Sending outreach campaign with {msg_count} messages")

            sent_count = 0
            failed_count = 0
            sent_messages = []

            for message in messages:
                try:
                    # Send email
                    result = await self.email_service.send_email(
                        to_email=message['contact_email'],
                        subject=message['subject'],
                        body=message['body']
                    )

                    if result.get('success'):
                        message['status'] = 'sent'
                        message['sent_at'] = datetime.utcnow().isoformat()
                        message['message_id'] = result.get('message_id')
                        sent_messages.append(message)
                        sent_count += 1
                    else:
                        message['status'] = 'failed'
                        message['error'] = result.get('error')
                        failed_count += 1

                except Exception as e:
                    contact = message['contact_email']
                    log.error(f"Failed to send message to {contact}: {e}")
                    message['status'] = 'failed'
                    message['error'] = str(e)
                    failed_count += 1

            # Build campaign result
            timestamp = datetime.utcnow().timestamp()
            campaign_result = {
                'total': len(messages),
                'sent': sent_count,
                'failed': failed_count,
                'messages': sent_messages,
                'auto_followup_enabled': auto_followup,
                'campaign_id': f"camp_{timestamp}",
                'completed_at': datetime.utcnow().isoformat()
            }

            # Log campaign completion
            log_msg = f"Campaign completed: {sent_count} sent"
            log.info(f"{log_msg}, {failed_count} failed")
            return campaign_result

        except Exception as e:
            log.error(f"Error sending outreach campaign: {e}")
            raise

    async def handle_response(
        self,
        response_text: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Handle lead responses and generate appropriate replies

        Args:
            response_text: Lead's response text
            conversation_history: Previous conversation messages

        Returns:
            Suggested response and next action
        """
        try:
            log.info("Processing lead response")

            # Analyze sentiment
            sentiment = await self.ai_service.analyze_sentiment(response_text)

            # Classify intent
            intent = await self.ai_service.classify_intent(response_text)

            # Determine next action
            action = self._determine_action(intent, sentiment)

            # Generate response if needed
            suggested_reply = None
            if action.get('requires_reply'):
                self._create_reply_prompt(
                    response_text,
                    conversation_history,
                    sentiment,
                    intent
                )
                lead_data = {
                    'prompt': 'reply_context'
                }
                suggested_reply = (
                    await self.ai_service.generate_outreach_content(
                        lead_data=lead_data,
                        context="email_reply",
                        provider_type="mock"
                    )
                )

            result = {
                'sentiment': sentiment,
                'intent': intent,
                'action': action,
                'priority': self._calculate_priority(sentiment, intent)
            }

            if suggested_reply:
                reply_content = suggested_reply.get('content')
                result['suggested_reply'] = reply_content

            action_type = action.get('type')
            msg = f"Response handled: intent={intent}, action={action_type}"
            log.info(msg)
            return result

        except Exception as e:
            log.error(f"Error handling response: {e}")
            raise

    async def send_followup(
        self,
        original_message: Dict[str, str],
        days_since_contact: int,
        provider_type: str = "mock"
    ) -> Dict[str, str]:
        """
        Generate and send follow-up message

        Args:
            original_message: Original outreach message
            days_since_contact: Days since last contact
            provider_type: AI provider to use

        Returns:
            Follow-up message
        """
        try:
            log.info(f"Generating follow-up (days: {days_since_contact})")

            # Adjust follow-up tone based on timing
            if days_since_contact <= 3:
                tone = "gentle"
            elif days_since_contact <= 7:
                tone = "professional"
            else:
                tone = "persistent"

            # Generate follow-up content
            followup_content = await self.ai_service.generate_outreach_content(
                lead_data={},
                context="followup_email",
                provider_type=provider_type
            )

            followup_message = {
                'in_reply_to': original_message.get('message_id'),
                'lead_id': original_message.get('lead_id'),
                'contact_email': original_message.get('contact_email'),
                'subject': f"Re: {original_message.get('subject')}",
                'body': followup_content.get('content', ''),
                'tone': tone,
                'status': 'draft',
                'followup_number': 1,
                'created_at': datetime.utcnow().isoformat()
            }

            log.info("Follow-up message generated")
            return followup_message

        except Exception as e:
            log.error(f"Error generating follow-up: {e}")
            raise

    async def _score_lead(self, lead: Dict[str, Any]) -> float:
        """Score a lead based on various factors (0-100)"""
        score = 50.0  # Base score

        # Increase score for complete information
        if lead.get('contact_name'):
            score += 10
        if lead.get('contact_email'):
            score += 15
        if lead.get('phone'):
            score += 10
        if lead.get('website'):
            score += 5

        # Industry match bonus
        if lead.get('industry'):
            score += 10

        return min(score, 100.0)

    def _create_subject_prompt(self, lead_data: Dict, tone: str) -> str:
        """Create prompt for subject line generation"""
        business = lead_data['business_name']
        industry = lead_data['industry']
        return f"""
        Generate a compelling email subject line for {business}
        in the {industry} industry. Tone: {tone}.
        Keep it under 50 characters and make it personalized.
        """

    def _create_body_prompt(
        self,
        lead_data: Dict,
        tone: str,
        goal: str
    ) -> str:
        """Create prompt for email body generation"""
        return f"""
        Write a personalized outreach email for {lead_data['contact_name']}
        at {lead_data['business_name']}. Industry: {lead_data['industry']},
        Location: {lead_data['location']}.

        Tone: {tone}
        Goal: {goal}

        Keep it concise (150-200 words), professional, and focused on value.
        """

    def _create_reply_prompt(
        self,
        response: str,
        history: List[Dict],
        sentiment: Dict,
        intent: str
    ) -> str:
        """Create prompt for generating reply to lead response"""
        return f"""
        Generate a professional reply to this lead response:
        "{response}"

        Sentiment: {sentiment}
        Intent: {intent}

        Consider the conversation context and maintain a helpful tone.
        """

    def _create_followup_prompt(
        self,
        original: Dict,
        days: int,
        tone: str
    ) -> str:
        """Create prompt for follow-up message"""
        orig_subject = original.get('subject')
        return f"""
        Write a {tone} follow-up email. Original subject: {orig_subject}.
        Days since last contact: {days}.

        Keep it brief and friendly.
        Reference the previous email without being pushy.
        """

    def _determine_action(
        self,
        intent: str,
        sentiment: Dict
    ) -> Dict[str, Any]:
        """Determine next best action based on intent and sentiment"""
        positive_threshold = 0.6

        is_negative = sentiment.get('negative', 0) > positive_threshold

        action_map = {
            'interested': {
                'type': 'schedule_meeting',
                'requires_reply': True,
                'priority': 'high'
            },
            'not_interested': {
                'type': 'mark_unqualified',
                'requires_reply': False,
                'priority': 'low'
            },
            'more_info': {
                'type': 'send_information',
                'requires_reply': True,
                'priority': 'medium'
            },
            'wrong_contact': {
                'type': 'update_contact',
                'requires_reply': False,
                'priority': 'low'
            },
            'out_of_office': {
                'type': 'wait_and_followup',
                'requires_reply': False,
                'priority': 'medium'
            }
        }

        default_action = {
            'type': 'followup_later',
            'requires_reply': True,
            'priority': 'medium'
        }
        base_action = action_map.get(intent, default_action)

        # Adjust for negative sentiment
        if is_negative:
            base_action['priority'] = 'low'
            base_action['type'] = 'pause_outreach'

        return base_action

    def _calculate_priority(self, sentiment: Dict, intent: str) -> str:
        """Calculate priority of response"""
        if intent == 'interested' or sentiment.get('positive', 0) > 0.7:
            return 'high'
        elif intent == 'not_interested' or sentiment.get('negative', 0) > 0.7:
            return 'low'
        else:
            return 'medium'


# Global agent instance
ai_lead_agent = AILeadAgent()
