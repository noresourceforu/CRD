import os
import ssl
import kopf
import aiohttp
from kubernetes import config
from kubernetes.client import Configuration

# Disable SSL verification for aiohttp (used internally by Kopf)
kopf.TCPConnector = lambda: aiohttp.TCPConnector(ssl=False)

# Optionally disable global SSL verification (not strictly necessary if aiohttp is patched)
ssl._create_default_https_context = ssl._create_unverified_context

# Load in-cluster config
config.load_incluster_config()

# Set up Kubernetes Python client config (not used by Kopf directly but good practice)
cfg = Configuration.get_default_copy()
cfg.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
os.environ['REQUESTS_CA_BUNDLE'] = cfg.ssl_ca_cert
Configuration.set_default(cfg)

# Register the operator handler
@kopf.on.create('jobrunners')
def create_fn(spec, **kwargs):
    image = spec.get('image')
    command = spec.get('command', [])
    print(f"🛠️ Creating job with image: {image} and command: {command}")
