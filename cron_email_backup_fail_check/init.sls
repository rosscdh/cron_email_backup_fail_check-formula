{% from "cron_email_backup_fail_check/map.jinja" import config with context %}
{% set docker_env = config['docker_env'] %}

{{ config['env_file'] }}:
  file.managed:
  - makedirs: true
  - contents: |
      {%- for key, value in docker_env.iteritems() %}
      {{ key }}={{ value }}
      {%- endfor %}

'docker run --rm -it --env-file {{ config["env_file"] }} {{ config["image"] }}':
  cron.present:
    - user: {{ config['user'] }}
    - minute: {{ config['minute'] }}
    - hour: {{ config['hour'] }}

