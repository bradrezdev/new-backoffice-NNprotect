"""
Script de prueba para verificar que el sistema UserTreePath funciona correctamente.
"""
import reflex as rx
from NNProtect_new_website.mlm_service.mlm_user_manager import MLMUserManager

def test_usertreepath():
    """Función para probar el sistema UserTreePath."""
    print("🧪 Iniciando prueba de UserTreePath...")
    
    # Simular la creación de un usuario con sponsor
    with rx.session() as session:
        try:
            # Test 1: Crear usuario MLM con sponsor
            print("\n1️⃣ Probando creación de usuario con sponsor...")
            import time
            unique_id = f"test-supabase-id-{int(time.time())}"
            new_user = MLMUserManager.create_mlm_user(
                session, 
                unique_id, 
                "Usuario", 
                "Prueba", 
                f"prueba{int(time.time())}@test.com", 
                1  # Sponsor con member_id 1 (Bryan)
            )
            
            session.commit()
            print(f"✅ Usuario creado: Member ID {new_user.member_id}")
            
            # Test 2: Verificar que se creó el UserTreePath
            from database.usertreepaths import UserTreePath
            import sqlmodel
            
            tree_path = session.exec(
                sqlmodel.select(UserTreePath).where(
                    UserTreePath.user_id == new_user.member_id
                )
            ).first()
            
            if tree_path:
                print(f"✅ UserTreePath creado correctamente:")
                print(f"   - Sponsor ID: {tree_path.sponsor_id}")
                print(f"   - User ID: {tree_path.user_id}")
            else:
                print("❌ UserTreePath NO se creó")
                
            # Test 3: Probar la consulta de red descendente
            print("\n2️⃣ Probando consulta de red descendente...")
            descendants = MLMUserManager.get_network_descendants(1)  # Red de Bryan (member_id 1)
            
            print(f"✅ Encontrados {len(descendants)} descendientes en la red:")
            for desc in descendants:
                print(f"   - {desc['first_name']} {desc['last_name']} (ID: {desc['member_id']})")
                
            # Test 4: Probar inscripciones del día
            print("\n3️⃣ Probando inscripciones del día...")
            todays_registrations = MLMUserManager.get_todays_registrations(1)
            
            print(f"✅ Encontradas {len(todays_registrations)} inscripciones del día:")
            for reg in todays_registrations:
                print(f"   - {reg['first_name']} {reg['last_name']} (ID: {reg['member_id']})")
                
        except Exception as e:
            print(f"❌ Error en la prueba: {e}")
            import traceback
            traceback.print_exc()
            session.rollback()

if __name__ == "__main__":
    test_usertreepath()