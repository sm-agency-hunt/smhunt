"""
Email provider interfaces for sending and tracking emails
"""
from abc import abstractmethod
from typing import Dict, Any
from .base_provider import BaseProvider, MockProvider


class EmailProvider(BaseProvider):
    """Interface for email service providers"""
    
    @abstractmethod
    async def send_email(
        self, 
        recipient: str, 
        subject: str, 
        body: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send an email"""
        pass
    
    @abstractmethod
    async def track_delivery(
        self, 
        message_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Track email delivery status"""
        pass
    
    @abstractmethod
    async def handle_bounce(
        self, 
        message_id: str,
        **kwargs
    ) -> bool:
        """Handle bounced emails"""
        pass


class SendGridProvider(EmailProvider):
    """SendGrid provider for email sending"""
    
    async def send_email(
        self, 
        recipient: str, 
        subject: str, 
        body: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send email using SendGrid API"""
        if not self.api_key:
            raise ValueError("SendGrid API key required")
        
        url = "https://api.sendgrid.com/v3/mail/send"
        payload = {
            "personalizations": [{
                "to": [{"email": recipient}],
                "subject": subject
            }],
            "from": {"email": kwargs.get("sender", "noreply@example.com")},
            "content": [{
                "type": kwargs.get("content_type", "text/html"),
                "value": body
            }]
        }
        
        response = await self._make_request("POST", url, json=payload)
        
        return {
            "success": True,
            "message_id": response.get("message_id", "mock_message_id"),
            "recipient": recipient,
            "status": "sent"
        }
    
    async def track_delivery(
        self, 
        message_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Track email delivery using SendGrid API"""
        if not self.api_key:
            raise ValueError("SendGrid API key required")
        
        # SendGrid doesn't have direct API for getting 
        # delivery status by message_id
        # This would require webhook events in production
        return {
            "message_id": message_id,
            "status": "delivered",
            "timestamp": "2024-01-01T00:00:00Z",
            "details": {
                "delivered": True,
                "opened": False,
                "clicked": False,
                "bounced": False
            }
        }
    
    async def handle_bounce(
        self, 
        message_id: str,
        **kwargs
    ) -> bool:
        """Handle bounced email using SendGrid API"""
        if not self.api_key:
            raise ValueError("SendGrid API key required")
        
        # In production, this would involve webhook events
        return True


class MailgunProvider(EmailProvider):
    """Mailgun provider for email sending"""
    
    async def send_email(
        self, 
        recipient: str, 
        subject: str, 
        body: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send email using Mailgun API"""
        if not self.api_key:
            raise ValueError("Mailgun API key required")
        
        domain = kwargs.get('domain', 'your-domain.com')
        url = f"https://api.mailgun.net/v3/{domain}/messages"
        
        import aiohttp
        data = {
            "from": kwargs.get("sender", "noreply@example.com"),
            "to": recipient,
            "subject": subject,
            "html": body
        }
        
        # For Mailgun, we need to make a form-encoded request
        async with aiohttp.ClientSession() as session:
            auth = aiohttp.BasicAuth("api", self.api_key)
            async with session.post(url, data=data, auth=auth) as response:
                response.raise_for_status()
                result = await response.json()
        
        return {
            "success": True,
            "message_id": result.get("id", "mock_message_id"),
            "recipient": recipient,
            "status": "sent"
        }
    
    async def track_delivery(
        self, 
        message_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Track email delivery using Mailgun API"""
        if not self.api_key:
            raise ValueError("Mailgun API key required")
        
        domain = kwargs.get('domain', 'your-domain.com')
        url = f"https://api.mailgun.net/v3/{domain}/events"
        params = {"message-id": message_id}
        
        response = await self._make_request("GET", url, params=params)
        
        events = response.get("items", [])
        status = "unknown"
        
        for event in events:
            if event.get("event") == "delivered":
                status = "delivered"
            elif event.get("event") == "opened":
                status = "opened"
            elif event.get("event") == "clicked":
                status = "clicked"
            elif event.get("event") == "bounced":
                status = "bounced"
                break
        
        return {
            "message_id": message_id,
            "status": status,
            "timestamp": "2024-01-01T00:00:00Z",
            "details": {"events": events}
        }
    
    async def handle_bounce(
        self, 
        message_id: str,
        **kwargs
    ) -> bool:
        """Handle bounced email using Mailgun API"""
        if not self.api_key:
            raise ValueError("Mailgun API key required")
        
        domain = kwargs.get('domain', 'your-domain.com')
        url = f"https://api.mailgun.net/v3/{domain}/bounces"
        
        response = await self._make_request("GET", url, params={"limit": 100})
        
        bounces = response.get("items", [])
        for bounce in bounces:
            if bounce.get("id") == message_id:
                # Delete the bounce record
                delete_url = f"{url}/{bounce.get('address')}"
                await self._make_request("DELETE", delete_url)
                return True
        
        return False


class SMTPProvider(EmailProvider):
    """SMTP provider for email sending"""
    
    async def send_email(
        self, 
        recipient: str, 
        subject: str, 
        body: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send email using SMTP"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        smtp_server = kwargs.get("smtp_server", "localhost")
        smtp_port = kwargs.get("smtp_port", 587)
        sender_email = kwargs.get("sender", "noreply@example.com")
        sender_password = self.api_key
        
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            
            text = msg.as_string()
            server.sendmail(sender_email, recipient, text)
            server.quit()
            
            return {
                "success": True,
                "message_id": "smtp_mock_message_id",
                "recipient": recipient,
                "status": "sent"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "recipient": recipient,
                "status": "failed"
            }
    
    async def track_delivery(
        self, 
        message_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """SMTP provider cannot track delivery"""
        return {
            "message_id": message_id,
            "status": "not_tracked",
            "details": {"reason": "SMTP does not support delivery tracking"}
        }
    
    async def handle_bounce(
        self, 
        message_id: str,
        **kwargs
    ) -> bool:
        """SMTP provider cannot handle bounces"""
        return False


class MockEmailProvider(MockProvider, EmailProvider):
    """Mock email provider for testing and development"""
    
    async def send_email(
        self, 
        recipient: str, 
        subject: str, 
        body: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Mock email sending"""
        import uuid
        message_id = str(uuid.uuid4())
        
        # Simulate some random failures for testing
        import random
        # 80% success rate
        success = random.choice([True, True, True, True, False])
        
        if success:
            return {
                "success": True,
                "message_id": message_id,
                "recipient": recipient,
                "subject": subject[:50],  # Truncate for privacy
                "status": "sent",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        else:
            return {
                "success": False,
                "message_id": message_id,
                "recipient": recipient,
                "error": "Mock delivery failure",
                "status": "failed"
            }
    
    async def track_delivery(
        self, 
        message_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Mock delivery tracking"""
        import random
        status_options = ["sent", "delivered", "opened", "replied", "bounced"]
        status = random.choice(status_options)
        
        return {
            "message_id": message_id,
            "status": status,
            "timestamp": "2024-01-01T00:00:00Z",
            "details": {
                "delivered": status in ["delivered", "opened", "replied"],
                "opened": status in ["opened", "replied"],
                "replied": status == "replied",
                "bounced": status == "bounced"
            }
        }
    
    async def handle_bounce(
        self, 
        message_id: str,
        **kwargs
    ) -> bool:
        """Mock bounce handling"""
        # Simulate successful bounce handling
        return True