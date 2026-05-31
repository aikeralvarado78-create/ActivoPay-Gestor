import pandas as pd
from sqlalchemy.orm import Session
from models import Empresa, Usuario, Gestion

def migrar_excel_a_bd(archivo_excel, session: Session):
    df = pd.read_excel(archivo_excel)
    
    for _, fila in df.iterrows():
        # 1. Crear o actualizar Empresa
        empresa = Empresa(
            rif=fila['RIF (Jxxxxxxx)'],
            nombre_empresa=fila['Nombre de la Empresa'],
            telefono_principal=str(fila['NRO DE TELEFONO Empresa (Principal)']),
            rubro=fila['Rubro (Razón económica)'],
            region=fila['Región'],
            ejecutivo_id=fila['Correo del Ejecutivo']
        )
        session.merge(empresa) # merge evita duplicados si el RIF ya existe
        
        # 2. Registrar Gestión Inicial
        gestion = Gestion(
            empresa_rif=fila['RIF (Jxxxxxxx)'],
            estatus=fila['Estatus'],
            fecha_recibido=fila['Fecha Recibido']
        )
        session.add(gestion)
        
        # 3. Procesar Usuarios (Aquí ocurre la "magia" de desanidar)
        # Asumimos que los usuarios vienen en bloques fijos en el Excel
        usuarios_data = [
            {'nombre': fila['Nombre y Apellido de la Persona del usuario Master (Principal)'], 
             'ci': fila['C.I Usuario Master (Principal)'], 
             'correo': fila['Correo Electrónico Usuario Master (Principal)'], 'rol': 'Master'},
            {'nombre': fila['Nombre y Apellido de la Persona del usuario Secundario'], 
             'ci': fila['C.I Secundario'], 
             'correo': fila['Correo Electrónico Usuario Secundario'], 'rol': 'Secundario'}
        ]
        
        for u in usuarios_data:
            if pd.notna(u['ci']): # Solo registra si hay cédula
                usuario = Usuario(
                    ci=str(u['ci']),
                    nombre_completo=u['nombre'],
                    correo=u['correo'],
                    rol=u['rol'],
                    empresa_rif=fila['RIF (Jxxxxxxx)']
                )
                session.merge(usuario)
    
    session.commit()
    print("Migración completada con éxito.")