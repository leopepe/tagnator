import boto3
import logging


class Tagnator:

    def __init__(self, log_level: str='INFO'):
        # Log setup
        # log constants
        __app_name = 'tagnator'
        __app_log_file = __app_name + '.log'
        __log_format = '%(asctime)s %(levelname)s %(message)s'

        # logger object
        self.log = logging.getLogger(__app_name)
        # log file handler
        __log_fh = logging.FileHandler(__app_log_file)
        __log_fh.setFormatter(logging.Formatter(__log_format))

        # set log level
        if log_level == 'INFO':
            self.log.setLevel(logging.INFO)
            __log_fh.setLevel(logging.INFO)
        elif log_level == 'DEBUG':
            self.log.setLevel(logging.DEBUG)
            __log_fh.setLevel(logging.DEBUG)
        elif log_level == 'WARNING':
            self.log.setLevel(logging.WARN)
            __log_fh.setLevel(logging.WARN)

        self.log.addHandler(__log_fh)

        self.ec2 = boto3.resource('ec2')
        self.volumes = self.ec2.volumes.all()

    def tag_volumes_by_key(self, key: str='project'):
        for vol in self.volumes:
            for attr in vol.attachments:
                instance_id = attr['InstanceId']
                tags = self.ec2.Instance(instance_id).tags
                self.log.debug(
                    'Instance id: {id}, {key}: {tags}'.format(id=instance_id, tags=tags, key=key)
                )
                for tag in tags:
                    self.log.debug('tag: {tag}'.format(tag=tag))
                    # check for tag key
                    if tag['Key'] == key:
                        self.log.info(
                            'Tagging volume: {vol_id} for {tagk} {tagv}'.format(vol_id=vol.id, tagk=key, tagv=tag['Value'])
                        )
                        vol.create_tags(Tags=[{'Key': 'project', 'Value': tag['Value']}])
                    else:
                        self.log.info('No tag key {key} found on the instance'.format(key=key))

    def volume_attachments(self):
        for vol in self.volumes:
            self.log.debug('Volumes attachments: {}'.format(vol.attachments))


if __name__ == '__main__':
    tag = Tagnator(log_level='DEBUG')
    tag.volume_attachments()
    # tag volumes by key
    tag.tag_volumes_by_key(key='project')
