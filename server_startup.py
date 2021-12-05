from app import create_app

# Create flask app object
application = create_app()


if __name__ == '__main__':
    # Run server
    application.run()
