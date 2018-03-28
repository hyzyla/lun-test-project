from catalog import app


def serve():
    app.run(debug=True)


if __name__ == '__main__':
    serve()