def register_helpers(app, services):
    @app.template_filter('toclass')
    def service_state_toclass_filter(s):
        if s == 'Stopped':
            return 'color-red'
        elif s == 'Running':
            return 'color-green'
        elif s == 'Not Installed':
            return 'color-gray'
        else:
            return ''
