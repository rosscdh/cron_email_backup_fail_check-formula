{% from "cron_email_backup_fail_check/map.jinja" import config with context %}
{% from "cron_email_backup_fail_check/map.jinja" import docker_env with context %}

{{ config['env_file'] }}:
  file.serialize:
  - makedirs: true
  - dataset: {{ docker_env }}

docker run --rm -it --env-file {{ config['env_file'] }} {{ config['image'] }}:
  cron.present:
    - user: {{ config['user'] }}
    - minute: {{ config['minute'] }}
    - hour: {{ config['hour'] }}

