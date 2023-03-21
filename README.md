# Music service (BMSTU Project) - BackEnd part
##### This is branch that contains API for FrontEnd part of the application, written on Python language
---
### Used modules:
* FastAPI (with Uvicorn)
* Tortoise orm[aiomysql]
* NumPy
* Pandas
* Sklearn
---
### Another services:
* Docker
* Swagger UI
---
## How to start
1. Clone repository branch by 
```console
git clone -b rec_service https://github.com/cherry4xo/school-project
```
2. In root directory of cloned repository run
```console
python -m venv venv
source venv/Scripts/activate
pip install fastapi tortoise-orm[aiomysql] librosa numpy==1.23.5 pandas sklearn yellowbrick scipy difflib pydantic
```
3. Install [Docker](https://www.docker.com/products/docker-desktop/)
4. In any command line go to the cloned repository and run in /docker directory run 
```console
docker-compose up -d
```
5. In rool directory of cloned repository run
```console
uvicorn main:app --host <host> --port <port> --reload
```
where `<host>` and `<port>` is desired host and port of your API
 
