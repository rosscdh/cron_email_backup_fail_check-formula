def test_file_exists(host):
    cron_email_backup_fail_check = host.file('/cron_email_backup_fail_check.yml')
    assert cron_email_backup_fail_check.exists
    assert cron_email_backup_fail_check.contains('your')

# def test_cron_email_backup_fail_check_is_installed(host):
#     cron_email_backup_fail_check = host.package('cron_email_backup_fail_check')
#     assert cron_email_backup_fail_check.is_installed
#
#
# def test_user_and_group_exist(host):
#     user = host.user('cron_email_backup_fail_check')
#     assert user.group == 'cron_email_backup_fail_check'
#     assert user.home == '/var/lib/cron_email_backup_fail_check'
#
#
# def test_service_is_running_and_enabled(host):
#     cron_email_backup_fail_check = host.service('cron_email_backup_fail_check')
#     assert cron_email_backup_fail_check.is_enabled
#     assert cron_email_backup_fail_check.is_running
