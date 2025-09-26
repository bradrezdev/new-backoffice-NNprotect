#!/usr/bin/env python3
"""
Script para probar el diccionario completo de usuario con SPONSOR
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar el sistema de conexión de Reflex
import reflex as rx
from NNProtect_new_website.mlm_service.mlm_user_manager import MLMUserManager

def test_user_with_sponsor():
    print("🧪 Probando usuario con sponsor...")
    
    try:
        # Importar las tablas necesarias
        from database.users import Users
        from database.usertreepaths import UserTreePath
        import sqlmodel
        
        # Buscar un usuario que tenga sponsor
        with rx.session() as session:
            # Primero buscar en UserTreePath un usuario con sponsor
            utp_result = session.exec(
                sqlmodel.select(UserTreePath)
                .where(UserTreePath.sponsor_id != None)
                .limit(1)
            ).first()
            
            if not utp_result:
                print("❌ No se encontró ningún UserTreePath con sponsor")
                return False
            
            # Ahora buscar el usuario correspondiente
            user = session.exec(
                sqlmodel.select(Users)
                .where(Users.member_id == utp_result.user_id)
            ).first()
            
            if not user:
                print("❌ No se encontró el usuario correspondiente")
                return False
                
            supabase_id = user.supabase_user_id
            member_id = user.member_id
            firstname = user.first_name
            lastname = user.last_name
            sponsor_id = utp_result.sponsor_id
            
            print(f"🔍 Encontrado usuario: {firstname} {lastname} (Member ID: {member_id}, Sponsor ID: {sponsor_id})")
            
    except Exception as e:
        print(f"❌ Error buscando usuario con sponsor: {e}")
        return False
    
    # Cargar datos completos
    if not supabase_id:
        print("❌ No se encontró supabase_id para el usuario")
        return False
        
    mlm_manager = MLMUserManager()
    user_data = mlm_manager.load_complete_user_data(supabase_id)
    
    if user_data:
        print("✅ Datos completos cargados exitosamente:")
        print(f"📋 DICCIONARIO COMPLETO:")
        
        import json
        print(json.dumps(user_data, indent=2, ensure_ascii=False))
        
        # Verificar campos específicos
        print(f"\n🎯 INFORMACIÓN DE SPONSOR:")
        if user_data.get('sponsor_info'):
            sponsor_info = user_data['sponsor_info']
            print(f"   - Sponsor Name: {sponsor_info.get('sponsor_name', 'N/A')}")
            print(f"   - Sponsor Member ID: {sponsor_info.get('sponsor_member_id', 'N/A')}")
        else:
            print("   - No tiene información de sponsor")
            
        print(f"✅ Total de campos: {len(user_data)}")
        return True
    else:
        print("❌ No se pudieron cargar los datos del usuario")
        return False

if __name__ == "__main__":
    try:
        success = test_user_with_sponsor()
        if success:
            print("\n🎉 Prueba con sponsor completada exitosamente")
        else:
            print("\n❌ Error en la prueba")
    except Exception as e:
        print(f"💥 Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()