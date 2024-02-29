# PHASE--5-SEV-0

# Table of Contents
* Introduction
* Description
* Installation
* Known Bugs
* Technologies used
* License

## Introduction

## Deliverables
## Models

The file `server/models.py` defines the model classes and its relationships**.
Use the following commands to create the initial database `test.db`:

```console
flask db upgrade 
```

The following relationships are implemented:




You can seed the database:

```console
python server/seed.py
```

> If you aren't able to get the provided seed file working, you are welcome to
> generate your own seed data to test the application.


## Routes

The following are the routes the application requires. 

![routes](/images/1.image.png.pdf)

![routes](/images/2.image.png.pdf)

![routes](/images/3.image.png.pdf)



## Set Up/ Installation 
- Clone the repository or download the source code.
- Make sure you have python or python3 installed on your system.
- Open the cloned folder with vscode.
To download the dependencies for the frontend and backend, run:

```console
pipenv install
pipenv shell
npm install --prefix client
```

You can run your Flask API on [`localhost:5000`](http://localhost:5000) by
running:

```console
python server/app.py
```

You can run your React app on [`localhost:4000`](http://localhost:4000) by
running:

```sh
npm start --prefix client
```

**Ensure your internet connection is stable to facilitate the download of the source code**


## Known Bugs
The application works well.

## Technologies used
- Terminal
- Python
- Flask
- JavaScript
- React

# License
This project is licensed under the MIT License.

