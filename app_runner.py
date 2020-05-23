import application


if __name__ == '__main__':
    instance = application.create_app()
    instance.run()