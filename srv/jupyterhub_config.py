
from jupyterhub.auth import DummyAuthenticator
from jinja2 import Template
import checkpoint_demo

# Not sure why this can't be set directly...
# It looks like it's a JupyterHub class property: https://github.com/jupyterhub/jupyterhub/blob/dac75ff996adb2831fcaeecb11811da1be8b03eb/jupyterhub/handlers/base.py#L764
# Learned about tornado_settings from https://github.com/jupyterhub/jupyterhub/issues/1222#issuecomment-320494512
c.JupyterHub.tornado_settings = {
    'slow_stop_timeout': 120
}

c.JupyterHub.spawner_class = checkpoint_demo.spawner.PodmanSpawner
c.JupyterHub.authenticator_class = DummyAuthenticator

c.PodmanSpawner.scheduler_image = "72522808"
c.PodmanSpawner.scheduler_region = "sfo3"
c.PodmanSpawner.scheduler_vpc = "ed580488-6eb8-4fc2-84e9-184502790372"
c.PodmanSpawner.scheduler_ssh_key = "/root/.ssh/id_rsa_podman.pub"
_sizes = [
    {
        "slug": "s-1vcpu-1gb",
        "description" : "Standard :: 1 CPU :: 1 GB RAM",
        "cpu" : 1,
        "memory" : 2**30
    },
    {
        "slug": "s-1vcpu-2gb",
        "description" : "Medium :: 1 CPU :: 2 GB RAM",
        "cpu" : 1,
        "memory" : 2 * 2**30
    },
    {
        "slug": "s-2vcpu-4gb",
        "description" : "Large :: 2 CPU :: 4 GB RAM",
        "cpu" : 2,
        "memory" : 4 * 2**30
    }
]
c.PodmanSpawner.sizes = _sizes

c.PodmanSpawner.options_form = Template("""
<div class='form-group' id='host-list'>
    <div class='col-md-12'>
        <strong>Hosts</strong>
    </div>
    {% for size in sizes %}
    <label for='host-{{ loop.index }}' class='form-control input-group'>
        <div class='col-md-1'>
            <input type='radio' name='host' id='host-{{ loop.index }}' value='{{ loop.index }}'{% if loop.index == 1 %} checked{% endif %} />
        </div>
        <div class='col-md-11'>
            {{ size.get('description') }}
        </div>
    </label>
    {% endfor %}
</div>
""").render(sizes=_sizes)

c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_connect_ip = "10.124.0.4"
# c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.command = [
    "configurable-http-proxy",
    "--ip=127.0.0.1",
    "--port=8000",
    "--api-ip=127.0.0.1",
    "--api-port=8001",
    "--default-target=http://localhost:8081",
    "--error-target=http://localhost:8081/hub/error"
]

c.JupyterHub.ssl_key = '/etc/letsencrypt/live/adass.dirac.institute/privkey.pem'
c.JupyterHub.ssl_cert = '/etc/letsencrypt/live/adass.dirac.institute/fullchain.pem'

c.JupyterHub.extra_handlers = [
    (
        r'/migrate', 
        checkpoint_demo.handler.migrate.MigrateHandler
        # dict(config=checkpoint_demo.handler.config.MigrateConfig())
    ),
    (
        r'/migrate/sizes', 
        checkpoint_demo.handler.sizes.SizesHandler, 
        dict(sizes=_sizes)
    )
]