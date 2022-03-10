import base64
import uuid

import boto3
from boto3 import s3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from odoo import models, api
import logging


class S3Attachment(models.Model):
    _inherit = 'ir.attachment'
    session = boto3.Session(
        aws_access_key_id="",
        aws_secret_access_key="",
    )
    try:
        resource = session.resource('s3')
    except BotoCoreError as exc:
        logging.exception(repr(exc))

    bucket_name = 'youngman-odoo'
    database_bucket = resource.Bucket(bucket_name)

    def object_exists(self, key):
        exists = True
        try:
            self.resource.Object(self.bucket_name, key).load()
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                exists = False
        return exists

    @api.model
    def _file_read(self, fname):
        _object = None
        file_exists = self.object_exists(fname)
        if not file_exists:
            _object = super(S3Attachment, self)._file_read(fname)
        else:
            s3_key = self.resource.Object(self.bucket_name, key=fname)
            _object = s3_key.get()['Body'].read()
        return _object

    @api.model
    def _file_write(self, bin_value, checksum):
        filename = str(uuid.uuid4())
        try:
            self.resource.Object(self.bucket_name, key=filename).put(Body=bin_value)
        #self.database_bucket.upload_fileobj(bin_value, filename)

        except Exception as exc:
            logging.exception(repr(exc))
        return filename
