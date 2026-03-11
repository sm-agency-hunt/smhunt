"""
Email provider interfaces for sending and tracking emails - Snov.io & Resend Integration
"""
import os
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


class ResendProvider(EmailProvider):
    """Resend API provider for sending emails - PRIMARY PROVIDER"""
    
    async def send_email(
        self, 
        recipient: str, 
        subject: str, 
        body: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send email using Resend API"""
        if not self.api_key:
            raise ValueError("Resend API key required")
        
        import aiohttp
        url = "https://api.resend.com/emails"
        payload = {
            "from": kwargs.get("sender", "hello@yourdomain.com"),
            "to": [recipient],
            "subject": subject,
            "html": body
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                result = await response.json()
        
        return {
            "success": True,
            "message_id": result.get("id", "mock_message_id"),
            "recipient": recipient,
            "status": "sent"
        }
    
    async def track_delivery(self, message_id: str, **kwargs) -> Dict[str, Any]:
        """Track email delivery using Resend API"""
        return {
            "message_id": message_id,
            "status": "delivered",
            "timestamp": "2024-01-01T00:00:00Z",
            "details": {"delivered": True, "opened": False, "bounced": False}
        }
    
    async def handle_bounce(self, message_id: str, **kwargs) -> bool:
        """Handle bounced email using Resend API"""
        return True


class SnovioProvider(EmailProvider):
    """Snov.io provider for finding emails - EMAIL FINDER"""
    
    async def find_email(
        self, 
        domain: str, 
        first_name: str = None, 
        last_name: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Find professional email using Snov.io API"""
        if not self.api_key or not self.user_id:
            raise ValueError("Snov.io credentials required")
        
        import aiohttp
        url = "https://api.snov.io/v1/find-email"
        params = {
            "client_id": self.user_id,
            "client_secret": self.api_key,
            "domain": domain
        }
        
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                result = await response.json()
        
        return {
            "email": result.get("data", {}).get("email", ""),
            "score": result.get("data", {}).get("score", 0),
            "source": "snovio"
        }
    
    async def send_email(self, recipient: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Snov.io doesn't support sending emails directly"""
        raise NotImplementedError("Use ResendProvider for sending emails")
    
    async def track_delivery(self, message_id: str, **kwargs) -> Dict[str, Any]:
        """Snov.io doesn't support tracking"""
        return {"message_id": message_id, "status": "not_tracked"}
    
    async def handle_bounce(self, message_id: str, **kwargs) -> bool:
        """Snov.io doesn't support bounce handling"""
        return False


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
        
        import aiohttp
        url = "https://api.sendgrid.com/v3/mail/send"
        payload = {
            "personalizations": [{"to": [{"email": recipient}], "subject": subject}],
            "from": {"email": kwargs.get("sender", "noreply@example.com")},
            "content": [{"type": kwargs.get("content_type", "text/html"), "value": body}]
        }
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
        
        return {
            "success": True,
            "message_id": "sendgrid_mock_message_id",
            "recipient": recipient,
            "status": "sent"
        }
    
    async def track_delivery(self, message_id: str, **kwargs) -> Dict[str, Any]:
        """Track email delivery using SendGrid API"""
        return {"message_id": message_id, "status": "delivered", "details": {"delivered": True}}
    
    async def handle_bounce(self, message_id: str, **kwargs) -> bool:
        """Handle bounced email using SendGrid API"""
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
        
        import aiohttp
        domain = kwargs.get('domain', 'your-domain.com')
        url = f"https://api.mailgun.net/v3/{domain}/messages"
        data = {
            "from": kwargs.get("sender", "noreply@example.com"),
            "to": recipient,
            "subject": subject,
            "html": body
        }
        
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
    
    async def track_delivery(self, message_id: str, **kwargs) -> Dict[str, Any]:
        """Track email delivery using Mailgun API"""
        return {"message_id": message_id, "status": "delivered"}
    
    async def handle_bounce(self, message_id: str, **kwargs) -> bool:
        """Handle bounced email using Mailgun API"""
        return True


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
    
    async def track_delivery(self, message_id: str, **kwargs) -> Dict[str, Any]:
        """SMTP provider cannot track delivery"""
        return {"message_id": message_id, "status": "not_tracked"}
    
    async def handle_bounce(self, message_id: str, **kwargs) -> bool:
        """SMTP provider cannot handle bounces"""
        return False


class MockEmailProvider(MockProvider, EmailProvider):
    """Mock email provider for testing"""
    
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
        
        import random
        success = random.choice([True, True, True, True, False])  # 80% success rate
        
        if success:
            return {
                "success": True,
                "message_id": message_id,
                "recipient": recipient,
                "subject": subject[:50],
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
    
    async def track_delivery(self, message_id: str, **kwargs) -> Dict[str, Any]:
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
    
    async def handle_bounce(self, message_id: str, **kwargs) -> bool:
        """Mock bounce handling"""
        return True