import yaml, os

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default


class Services(object):

    # Transient state
    STATE_INSTALLING = 'installing'
    STATE_UNINSTALLING = 'uninstalling'
    STATE_STOPPING = 'stopping'

    # Long live state
    STATE_RUNNING = 'running'
    STATE_STOPPED = 'stopped'
    STATE_NOT_INSTALLED = 'not installed'

    def __init__(self, docker_client, cfg_file = None):
        self.docker = docker_client
        if cfg_file:
            with open(cfg_file, 'r') as ymlfile:
                self.cfg = yaml.load(ymlfile)
        else:
            self.cfg = {'services':[]}

    def by_id(self, service_id):
        services = [s for s in self.cfg['services'] if s['id'] == service_id]
        if(len(services) > 0):
            return services[0]
        else:
            return None

    def docker_state(self):
        images = self.docker.images(name = '*tsp*')
        containers = self.docker.containers()

        return {'images': images, 'containers': containers}

    def state(self, service):
        containers = self.docker.containers()
        imageNok = True
        containersNok = True

        # search for image in docker
        for srv in service['stack']:
            image = srv['image']
            image_name = image.split(':')[0]
            img = get_first(self.docker.images(name = image_name))
            imageNok &= ( img == None )

            # Is there a running container associated to this image ?
            for container in containers:
                containersNok &= (container['Image'] != image)

        if(imageNok):
            return self.STATE_NOT_INSTALLED
        elif(containersNok):
            return self.STATE_STOPPED
        else:
            return self.STATE_RUNNING

    def states(self):
        services = []

        for service in self.cfg['services']:
            services.append({
                'completeName': service['completeName'],
                'id':       service['id'],
                'state':    self.state(service).title()
                })

        return {'services': services}

    def change(self, service_id, new_state):
        service = self.by_id(service_id)
        state = self.state(service)

        if(new_state == state):
            return service_id + ' is already in the given state ('+new_state+')'
        elif(new_state == self.STATE_RUNNING):
            return self.run(service)
        elif(new_state == self.STATE_STOPPED):
            if(state == self.STATE_NOT_INSTALLED):
                return self.install(service)
            else:
                return self.stop(service)
        elif(new_state == self.STATE_NOT_INSTALLED):
            return self.uninstall(service)
        else:
            return 'The given state ('+new_state+') is incorrect.'

    def install(self, service):
        """ Install the service configured in the configuration file. This method
        assume that the service is currently not installed on the host.
        from a docker pov, this method pull the required images and create the
        containers without starting these containers.

        Arguments:
        service -- the representation of the service defined in the configuration file
        """
        val = []
        for stack in service['stack']:
            image = stack['image'] if 'image' in stack else None
            environment = stack['environment'] if 'environment' in stack else None

            if 'ports' in stack:
                ports = []
                for p in stack['ports']:
                    ports.append(p.split(':')[1])
            else:
                ports = None

            if 'volumes' in stack:
                volumes = []
                for v in stack['volumes']:
                    volumes.append(os.path.abspath(v.split(':')[0]))
            else:
                volumes = None

            val.append(self.docker.create_container(
                name = stack['containerName'],
                image = image,
                environment = environment,
                ports = ports,
                volumes = volumes
            ))
        return val

    def uninstall(self, service):
        """ Uninstall the given service as described in the configuration file.
        This method assumes the service is installed.
        From a docker pov, this method stopped running containers and then remove
        the associated images.

        Arguments:
        service -- the representation of the service defined in the configuration file
        """
        self.stop(service)

        for stack in service['stack']:
            self.docker.remove_image(image = stack['image'])

    def stop(self, service):
        """
        Stop the given service as described in the configuration file. This method
        assumes the service is running.
        From a Docker pov, this method stopped all running containers.

        Arguments:
        service -- the representation of the service defined in the configuration file
        """
        for stack in service['stack']:
            self.docker.stop(container = stack['containerName'])

    def run(self, service):
        """
        Run the given service as described in the configuration file. This method
        assumes the service is installed.
        From a docker pov, thes method start all containers.

        Arguments:
        service -- the representation of the service defined in the configuration file
        """
        for stack in service['stack']:
            if 'links' in stack:
                links = []
                for l in stack['links']:
                    links.append((l,l))
            else:
                links = None


            if 'ports' in stack:
                ports = {}
                for p in stack['ports']:
                    ps = p.split(':')
                    ports[int(ps[1])] = int(ps[0])
            else:
                ports = None

            if 'volumes' in stack:
                binds = {}
                for v in stack['volumes']:
                    vs = v.split(':')
                    binds[vs[1]] = {
                        'bind': os.path.abspath(vs[0])
                    }
            else:
                binds = None

            self.docker.start(
                container = stack['containerName'],
                links = links,
                port_bindings = ports,
                binds = binds
            )
