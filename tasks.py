from invoke import task
import why82.infrastructure.deploy_stack as inf
import why82.settings as settings
from why82.s3_recorder import S3Recorder


@task
def test(ctx):
    ctx.run('nosetests --with-coverage --cover-package=why82 --cover-inclusive --cover-erase')


@task
def deps(ctx):
    ctx.run('vagrant up')
    ctx.run('./deps_pull.sh')
    ctx.run('vagrant destroy -f')


@task
def rm(ctx):
    inf.delete_stack()


@task
def crt(ctx):
    inf.create_stack()


@task
def updt(ctx):
    inf.update_stack()


@task()
def json(ctx):
    print(inf.create_template().to_json())

@task
def season(ctx):
    print(settings.CURRENT_SEASON)


@task
def update_data(ctx):
    stat_files = filter(lambda x :x.endswith('-stats.json'), S3Recorder.list_season_files(settings.CURRENT_SEASON, settings.STATS_BUCKET_NAME))
    import calc_schedule
    import calc_tiers
    for stat_key in stat_files:
        tiers_key = stat_key.replace('-stats.json', '-tiers.json')
        schedule_key = stat_key.replace('-stats.json', '-schedule.json')
        S3Recorder.rm_file(tiers_key, settings.BUCKET_NAME)
        print 'Deleted', tiers_key
        S3Recorder.rm_file(schedule_key, settings.BUCKET_NAME)
        print 'Deleted', schedule_key
        calc_tiers.lambda_handler({'Records':[{'s3':{'object':{'key': stat_key}}}]}, {})
        print 'Created', tiers_key
        calc_schedule.lambda_handler({'Records':[{'s3':{'object':{'key': tiers_key}}}]}, {})
        print 'Created', schedule_key
