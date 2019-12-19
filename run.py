from app import create_app
# from Lost_And_Found.config import ProductionConfig

app = create_app('config.ProductionConfig')


if __name__ == "__main__":
    from app.user import userbp
    from app.item import itembp

    app.register_blueprint(userbp)
    app.register_blueprint(itembp)
    app.run(host="0.0.0.0", debug=True)
