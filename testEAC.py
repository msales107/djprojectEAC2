# --- Mar Sales Alegre MP03 EAC2 25-10-25
# --- Tasca Personalitzada Selenium: Accés NO Autoritzat Admin

# En aquesta tasca, creem un usuari sense cap grup ni permís especial. 
# Després, comprovem que apareix a la llista d'usuaris 
# Per acabar comprovem que si intenta logar-se al /admin no pot entrar.

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

#Lliberia per la gestio dels usuaris
from django.contrib.auth.models import User
#Llibreria per la cerca de excepcions 
from selenium.common.exceptions import NoSuchElementException

class MySeleniumTests(StaticLiveServerTestCase):
    # no crearem una BD de test en aquesta ocasió (comentem la línia)
    #fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

        # creem usuari sense cap grup ni permís especial
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.save()

    def test_login(self):

        #Verifiquem si el usari existeix i si es actiu
        if User.objects.get(username='isard'):
           print("L'usuari aparèix al llistat d'usuaris i està actiu!")
        else:
           print("L'usuari aparèix al llistat d'usuaris")

        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        #Busquem que el usuari esta en la pantalla de login de usuaris administradors
        self.assertEqual( self.selenium.title , "Iniciar sesión | Sitio de administración de Django" )

        #Introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Iniciar sesión"]').click()

        try:
            # Creem una excepció en la que si es troba el lloc administratiu,
            # Al utilitzar una exception, si el find_element funciona, forcem un AssertionError (l'element no s'hauria d'haver trobat). 
            # L'except només captura l'excepció NoSuchElementException de Selenium, i en tal cas no farem res i seguim amb l'execució (l'element no hi és).
            
            #En aquest cas, busquem que la pàgina sigui la de Admin, si no es la de Admin
            #Executem el assert i el test passa al ser true

            #Si no es troba la excepcció, el test falla i per tant l'usuari ha entrat a Admin

            self.assertNotEqual( self.selenium.title , "Sitio administrativo | Sitio de administración de Django" )
            assert True, "L'Usuari NO ha pogut fer login a Admin!"
        except NoSuchElementException:
            print("L'Usuari ha pogut fer login a admin")
