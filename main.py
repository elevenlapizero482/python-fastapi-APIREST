from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#inicializamos una variable que tendra todas las caracteristicas de un API REST
app = FastAPI()

#aqui definimos el modelo
    # from   pydantic
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str#from typing
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

#simularemos base de datos

cursos_db = []

#CRUD: Read (lectura) GET ALL: leeremos todos  los cursos que hay en la base de datos
@app.get("/cursos/",response_model=List[Curso])
def obtener_cursos():
    return cursos_db

#CRUD: Create(escribir) POST: agregaremos un nuevo recurso a nuestra base de datos.
@app.post("/cursos/",response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) #crea un uuid aleatorio
    cursos_db.append(curso)
    return curso

#CRUD: Read (lectura) GET (individual) :Leeremos el curso con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso_id == curso.id), None) # con next sol ose toma laprimera coincidecia.
    if curso is None:
        raise HTTPException(status_code=404, detail="curso no encontrado")
    return curso

#CRUD: Update  (Actualizar/Modificar) PUT: Modificaremos un recurso que coincida con el id que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso_id == curso.id), None) # con next sol ose toma laprimera coincidecia.
    if curso is None:
        raise HTTPException(status_code=404, detail="curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # buscamos el indice exacto donde esta el curso en nuestra lista (DB)
    cursos_db[index] = curso_actualizado
    return curso_actualizado
#CRUD: Delete (borrar) :Eliminaremos un curso que coincida con el ID que mandemos.
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso_id == curso.id), None) # con next sol ose toma laprimera coincidecia.
    if curso is None:
        raise HTTPException(status_code=404, detail="curso no encontrado")
    cursos_db.remove(curso)
    return curso