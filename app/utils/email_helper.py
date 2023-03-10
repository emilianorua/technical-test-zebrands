from typing import List
from flask import current_app
import boto3
from app.repositories.user import UserRepository


class EmailHelper():

    @classmethod
    def get_ses_client(cls):
        if not current_app.config.get('ses_client', None):
            ses_client = boto3.client(
                "ses",
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
                region_name="us-west-2"
            )

            current_app.config['ses_client'] = ses_client

        return current_app.config['ses_client']

    @classmethod
    def send_verification_email(cls, email: str) -> None:
        if current_app.config['ENV'] != 'DEBUG':
            return
        
        ses_client = cls.get_ses_client()

        try:
            status = cls.get_verification_status(email)

            if status != 'Success':
                ses_client.verify_email_identity(EmailAddress=email)
        except Exception as e:
            print(f'Error on EmailHelper.send_verification_email() - {str(e)}')

    @classmethod
    def get_verification_status(cls, email: str) -> str:
        if current_app.config['ENV'] != 'DEBUG':
            return 'Success'

        ses_client = cls.get_ses_client()
        status = 'NotFound'
        try:
            response = ses_client.get_identity_verification_attributes(
                Identities=[email]
            )

            status = response['VerificationAttributes'].get(
                email,
                {'VerificationStatus': 'NotFound'}
            )['VerificationStatus']

        except Exception as e:
            print(f'Error on EmailHelper.get_verification_status() - {str(e)}')

        return status
    
    @classmethod
    def get_verified_emails(cls, emails: List[str]) -> List[str]:
        verified_emails = []

        for email in emails:
            if cls.get_verification_status(email) == 'Success':
                verified_emails.append(email)
        
        return verified_emails

    @classmethod
    def send_email(cls, subject: str, text: str, destinations: List[str] = None, to_admins: bool = False, user_public_id: str = None) -> None:
        if to_admins:
            destinations = UserRepository.get_admins_emails(user_public_id)
        
        verified_emails = cls.get_verified_emails(destinations)

        send_args = {
            'Source': current_app.config['SES_EMAIL'],
            'Destination': {
                'ToAddresses': verified_emails
            },
            'Message': {
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {
                        'Data': text
                    }
                }
            }
        }

        try:
            ses_client = cls.get_ses_client()
            response = ses_client.send_email(**send_args)
        except Exception as e:
            print(f'Error on EmailHelper.send_email() - {str(e)}')
