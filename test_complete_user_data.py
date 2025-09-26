"""
Script de prueba para verificar el diccionario completo de usuario.
"""
import reflex as rx
from NNProtect_new_website.mlm_service.mlm_user_manager import MLMUserManager
import json

def test_complete_user_data():
    """Función para probar el diccionario completo de usuario."""
    print("🧪 Iniciando prueba del diccionario completo de usuario...")
    
    try:
        # Usar el supabase_user_id del usuario Bryan (de las pruebas anteriores)
        supabase_user_id = "48c70885-db5c-41ab-9907-8775eb6a2e5c"
        
        print(f"\n🔄 Cargando datos completos para Supabase ID: {supabase_user_id}")
        
        # Cargar todos los datos del usuario
        complete_data = MLMUserManager.load_complete_user_data(supabase_user_id)
        
        if complete_data:
            print(f"\n✅ Datos completos cargados exitosamente:")
            print(f"📋 DICCIONARIO COMPLETO:")
            print(json.dumps(complete_data, indent=2, ensure_ascii=False, default=str))
            
            print(f"\n🎯 CAMPOS ESPECÍFICOS:")
            print(f"   - ID: {complete_data.get('id')}")
            print(f"   - Member ID: {complete_data.get('member_id')}")
            print(f"   - Username: {complete_data.get('username')}")
            print(f"   - First Name: {complete_data.get('firstname')}")
            print(f"   - Last Name: {complete_data.get('lastname')}")
            print(f"   - Full Name: {complete_data.get('full_name')}")
            print(f"   - Profile Name: {complete_data.get('profile_name')}")
            print(f"   - Email Cache: {complete_data.get('email_cache')}")
            print(f"   - Phone: {complete_data.get('phone')}")
            print(f"   - Status: {complete_data.get('status')}")
            print(f"   - Created At: {complete_data.get('created_at')}")
            print(f"   - Referral Link: {complete_data.get('referral_link')}")
            
            # Información del sponsor
            sponsor_info = complete_data.get('sponsor_info', {})
            if sponsor_info:
                print(f"\n👥 INFORMACIÓN DEL SPONSOR:")
                print(f"   - Sponsor Name: {sponsor_info.get('sponsor_name')}")
                print(f"   - Sponsor Member ID: {sponsor_info.get('sponsor_member_id')}")
            else:
                print(f"\n👥 SPONSOR: No tiene sponsor")
                
            # Información de dirección
            address = complete_data.get('address', {})
            if address and any(address.values()):
                print(f"\n🏠 DIRECCIÓN:")
                print(f"   - Street: {address.get('street')}")
                print(f"   - City: {address.get('city')}")
                print(f"   - State: {address.get('state')}")
                print(f"   - Country: {address.get('country')}")
            else:
                print(f"\n🏠 DIRECCIÓN: No registrada")
                
            print(f"\n✅ Prueba completada exitosamente")
            print(f"🎉 El diccionario contiene {len(complete_data)} campos")
            
        else:
            print("❌ No se pudieron cargar los datos del usuario")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_user_data()