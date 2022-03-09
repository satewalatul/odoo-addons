import base64
import uuid

import boto3
from boto3 import s3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from odoo import models, api
import logging


class S3Attachment(models.Model):
    _inherit = 'ir.attachment'

    # try:
    resource = boto3.resource('s3')
    # except BotoCoreError as exc:
    #    logging.exception(repr(exc))

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

    def put_object(self, key, mimetype="", body="", tags=""):
        #try:
        self.database_bucket.put_object(
            ACL="private",
            Body=body,
            Key=key,
            ContentType=mimetype,
            CacheControl="public, max-age=31536000"
            if body else "",
            Tagging=tags
        )
        #except NoCredentialsError as exc:
        #_logger.exception(repr(exc))
        #except ClientError as exc:
        #_logger.exception(repr(exc))
        #except BotoCoreError as exc:
        #_logger.exception(repr(exc))

    @api.model
    def _file_read(self, fname):
        _object = None
        file_exists = self.object_exists(fname)
        if not file_exists:
            _object = super(S3Attachment, self)._file_read(fname)
        else:
            s3_key = self.resource.Object(self.bucket_name, key=fname)
            _object = base64.b64encode(s3_key.get()['Body'].read())
        return _object

    @api.model
    def _file_write(self, value, checksum):
        # uuid is used for filename to prevent duplicates
        filename = str(uuid.uuid4())
        bin_value = base64.b64decode(value)
        # try:
        self.put_object(key=filename, body=bin_value)
        #self.resource.Object(self.bucket_name, key=filename).put(Body=bin_value)
        # except Exception as exc:
        #    logging.exception(repr(exc))
        return filename
