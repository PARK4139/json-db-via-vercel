# from app.routes import index, auth
import json
import logging
import os
from pathlib import Path
from typing import Union

import uvicorn
from fastapi import FastAPI, Request, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse


def import_pkg_park4139():  # 명령어 자체가 안되는데 /mir 은 되는데 /move 안된다
    # try:
    # 파이썬 프로젝트 외부 패키지 import 시키는 방법 : 일반적으로는 불가능하다.
    # services_directory_abspath = os.path.dirname(os.path.dirname(__file__))
    # external_pkg_abspath = rf'{services_directory_abspath}\archive_py\pkg_park4139'
    # print(rf'external_pkg_abspath : {external_pkg_abspath}')
    # os.environ['PKG_PARK4139_ABSPATH'] = rf'{external_pkg_abspath}'
    # sys.path.append(external_pkg_abspath)
    # print(rf'sys.path : {sys.path}')
    # from ..archive_py.pkg_park4139 import FileSystemUtil, StateManagementUtil, TestUtil
    # except:
    #     pass
    # try:
    # 대안 global pkg 로 복사하고 쓰고 실행후에는 프로젝트 내에서 패키지를 삭제한다 > 자동화할것
    # 의존성을 추가하기 위해서, pkg_park4139의 .venv 도 따라 복사한다.
    # CURRENT_PROJECT_DIRECTORY= os.path.dirname(__file__)
    # SERVICES_DIRECTORY = os.path.dirname(CURRENT_PROJECT_DIRECTORY)
    # EXTERNAL_PKG_ABSPATH = rf'{SERVICES_DIRECTORY}\archive_py\pkg_park4139'
    # # VIRTUAL_PKG_ABSPATH = rf'{CURRENT_PROJECT_DIRECTORY}\.venv\Lib\site-packages'
    # INTERNAL_PKG_ABSPATH = rf'{CURRENT_PROJECT_DIRECTORY}\pkg_park4139'
    # print(rf'VIRTUAL_PKG_ABSPATH : {INTERNAL_PKG_ABSPATH}')
    # os.system(rf'chcp 65001')
    # os.system(rf'robocopy "{EXTERNAL_PKG_ABSPATH}" "{INTERNAL_PKG_ABSPATH}" /MIR')
    # # os.system("pause")
    # print("파이썬 프로젝트 외부 패키지 import 시도에 성공하였습니다")
    # except Exception:
    #     print("파이썬 프로젝트 외부 패키지 import 시도에 실패하였습니다")
    #     sys.exit()
    # try:
    # 그냥 pkg 내에 집어 넣었다. 가상환경도 동일하게 개발한다.
    # except:
    #     pass
    pass


def convert_file_from_cp_949_to_utf_8(file_abspath):
    # import codecs
    # file_abspath_converted = rf"{FileSystemUtil.get_target_as_pn(file_abspath)}_utf_8{FileSystemUtil.get_target_as_x(file_abspath)}"
    # print(file_abspath_converted)
    # # 기존 파일을 'utf-8'로 읽어오고, 새로운 파일에 'utf-8'로 저장
    # with codecs.open(file_abspath, 'r', encoding='cp949') as file_previous:
    #     contents = file_previous.read()
    #     with codecs.open(file_abspath_converted, 'w', encoding='utf-8') as new_file:
    #         new_file.write(contents)
    pass

# :: SERVER SETTING
app = FastAPI()
app.encoding = 'utf-8'
os.system("chcp 65001")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# web_server_config = {
    # :: PRODUCTION MODE SETTING
    # 'port': 8080,
    # 'port': 80,
    # 'host': "0.0.0.0",

    # :: DEVELOPMENT MODE SETTING
    # 'port': 9002,
    # 'host': "127.0.0.1",
    # 'host': "localhost",
# }
DB_JSON = rf"{str(Path(__file__).parent.absolute())}\db.json"
print(DB_JSON)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# logger.addHandler(console_handler)

# CORS 설정 via add_middleware(), origins
origins = [
    # DEV
    "*",
    #     "http://localhost.tiangolo.com",
    #     "https://localhost.tiangolo.com",
    #     "http://localhost",
    #     "http://localhost:8080",
    # "http://localhost:3000",  # client 의 설정     "127.0.0.1:11430" next.js 이렇게 실행되는데?
    #
    # OP
    #
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # cookie 포함 여부를 설정. 기본은 False
    allow_methods=["*"],  # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다. OPTIONS request ?
    allow_headers=["*"],  # 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)


# 미들웨어를 통한 로깅
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.debug(f"요청: {request.method} {request.url}")
    response = await call_next(request)
    logging.debug(f"응답: {response.status_code}")
    return response


@app.get("/")
async def return_success():
    return { "success":"json-db 가 정상 동작 중 입니다"}


@app.get("/{specific_object_name}")
async def get_specific_object_json_db(specific_object_name):
    '''python json 파일에서 특정 객체만 추출'''
    logging.debug(rf'specific_object_name : {specific_object_name}')
    file = open(DB_JSON, encoding="utf-8")
    try:
        object_specific = json.load(file)[specific_object_name]
        object_specific = JSONResponse(object_specific)
    except KeyError:
        logging.debug("json db 에서 해당 객체는 존재하지 않습니다")
        # return {"error": "json db 에서 해당 객체는 존재하지 않습니다"}
        return None
    return object_specific


# Pydantic은 Python의 데이터 유효성 검사 및 직렬화를 위한 라이브러리로,
# 데이터 모델을 정의하고 유효성을 검사하며 직렬화/역직렬화를 수행하는 기능을 제공합니다
# auto increment 하고 싶어 pydantic model 로 구현
import json

def get_max_id_from_database():
    # db.json 파일을 UTF-8 인코딩으로 읽어옴
    with open(DB_JSON, 'r', encoding='utf-8') as file:
        data = json.load(file)
        boards = data.get('boards', [])
    if boards:
        # boards 객체가 존재하는 경우 최대 ID를 조회
        max_id = max(board['id'] for board in boards)
        return max_id
    else:
        # boards 객체가 없는 경우 None 반환
        return None
def some_function_to_generate_auto_increment_id():
    # 데이터베이스에서 현재의 최대 ID 조회
    max_id = get_max_id_from_database()  # 데이터베이스에서 최대 ID를 조회하는 함수로 구현되어야 합니다.

    if max_id is not None:
        # 최대 ID가 존재하는 경우 다음 ID를 생성하여 반환
        next_id = max_id + 1
    else:
        # 최대 ID가 없는 경우 1부터 시작
        next_id = 1
    return next_id
class Board(BaseModel):
    id: int = Field(default_factory=lambda: some_function_to_generate_auto_increment_id(), alias="_id")
    title: str
    content: str
    class Config:
        populate_by_name = True

def is_valid(board: Board) -> bool:
    # 게시물의 유효성을 검사하는 로직을 구현
    # 유효성 검사에 실패한 경우 False를 반환, 성공한 경우 True를 반환
    if not board.title:
        return False
    if not board.content:
        return False
    return True


@app.post("/files/")
async def create_file(file: UploadFile):
    content = await file.read()

    return JSONResponse({"filename": file.filename})


@app.post("/boards",response_class=JSONResponse)
async def create_board(board: Board):
    # logging.debug("1")
    # logging.debug(board)
    # board = JSONResponse(board)

    # 유효성 검사
    if not is_valid(board):
        raise HTTPException(status_code=422, detail="게시물 유효성 검사에 실패했습니다.")


    # 새로운 게시물 객체 생성
    new_board = {
        # "id": board.id,
        "title": board.title,
        "content": board.content
    }

    # db.json 파일에서 기존 데이터 로드
    with open(DB_JSON, "r") as file:
        data = json.load(file)

    # 새로운 게시물 추가
    data.append(new_board)

    # db.json 파일에 데이터 저장
    with open(DB_JSON, "w") as file:
        json.dump(data, file, indent=4)
    return JSONResponse(content={"message": "게시물이 성공적으로 생성되었습니다."})


# @app.get("/{recipe}")
# async def getSpecialJsonFile(recipe):
#     if os.path.exists(rf'{PROJECT_DIRECTORY}\{recipe}.json'):
#         with open(f'{recipe}.json') as file:
#         return json.load(file,encoding="utf-8")
#     else:
#         return {"Error":"요청하신 json 파일이 서버에 없습니다(FILE NOT FOUND" }
#
#
# @app.get("/{recipe}")
# async def getSpecialJsonFile(recipe):
#     if os.path.exists(rf'{PROJECT_DIRECTORY}\{recipe}.json'):
#         with open(f'{recipe}.json') as file:
#         return json.load(file,encoding="utf-8")
#     else:
#         return {"Error":"요청하신 json 파일이 서버에 없습니다(FILE NOT FOUND" }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



if __name__ == "__main__":
    # :: ASGI SERVER RUN SETTING
    os.system("ASGI SERVER RUN....VIA uvicorn")
    print(f'BASE_DIR : {BASE_DIR}')
    print(f'web_server_config["host"] : {web_server_config["host"]}')
    print(f'web_server_config["port"] : {web_server_config["port"]}')
    uvicorn.run(
        app="json_db:app",
        host=web_server_config['host'],
        port=web_server_config['port'],
        reload=True,
        log_level="debug",
    )

