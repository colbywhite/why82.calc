from invoke import task
import why82.infrastructure.deploy_stack as inf
import why82.settings as settings


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
