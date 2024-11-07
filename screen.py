import pygame
import sys
import webview
import folium
from selenium import webdriver
from abc import ABC, abstractmethod
import webbrowser

class RouteDisplay(ABC):
    @abstractmethod
    def display_route(self, route):
        pass


def save_map_as_image(map_path, output_image_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Налаштуйте шлях до вашого драйвера Chrome
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('file://' + map_path)

    time.sleep(2)  # Зачекайте, поки сторінка завантажиться

    screenshot = driver.get_screenshot_as_png()

    image = Image.open(io.BytesIO(screenshot))
    image.save(output_image_path)

    driver.quit()

class MapRouteDisplay(RouteDisplay):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        folium_map = folium.Map(location=[50.4501, 30.5234], zoom_start=12)
        for stop in stops:
            folium.Marker(location=stop, popup="Зупинка").add_to(folium_map)
        folium.PolyLine(locations=stops, color='blue', weight=5, opacity=0.8).add_to(folium_map)

        # Зберігаємо карту в файл HTML і відкриваємо у веб-браузері
        folium_map.save("route_map.html")
        webbrowser.open("route_map.html")

    def create_map(self, stops):
        # Додавання маркерів для зупинок
        for stop in stops:
            folium.Marker(location=stop, popup="Зупинка").add_to(self.map)

        # Додавання лінії між зупинками
        folium.PolyLine(locations=stops, color='blue', weight=5, opacity=0.8).add_to(self.map)

        # Збереження карти як HTML
        self.map.save("map.html")

    def get_map_image(self):
        # Ініціалізація Selenium для відображення карти
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--window-size=800,600")
        driver = webdriver.Chrome(options=options)

        # Відкриття збереженого HTML файлу з картою
        driver.get("file://" + sys.path[0] + "/map.html")
        driver.save_screenshot("map_screenshot.png")
        driver.quit()


class ListRouteDisplay(RouteDisplay):
    def __init__(self, screen, font, color):
        self.screen = screen
        self.font = font
        self.color = color
        self.start_y = 120

    def display_route(self, route):
        route_text_surface = self.font.render(f"{route['number']} - {route['route']}", True, self.color)
        self.screen.blit(route_text_surface, (20, self.start_y))

        # Створення кнопки "Відстежити"
        track_button_surface = self.font.render("Відстежити", True, (0, 0, 255))
        track_button_rect = track_button_surface.get_rect(topleft=(650, self.start_y))
        self.screen.blit(track_button_surface, track_button_rect.topleft)
        route['track_button'] = track_button_rect

        self.start_y += 50


class TransportApp:
    def __init__(self):
        pygame.init()

        # Параметри вікна
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Транспорт і Маршрути")

        # Кольори
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_GRAY = (220, 220, 220)
        self.DARK_GRAY = (169, 169, 169)

        # Завантаження зображень
        self.trolleybus_image = pygame.image.load("tram.png")
        self.flag_image = pygame.image.load("flag.png")
        self.trolleybus_image = pygame.transform.scale(self.trolleybus_image, (512, 170))
        self.flag_image = pygame.transform.scale(self.flag_image, (100, 100))

        # Позиції зображень
        self.trolleybus_rect = self.trolleybus_image.get_rect(center=(self.width // 2, self.height // 2))
        self.flag_rect = self.flag_image.get_rect(center=(self.width // 2, 100))
        self.trolleybus_dx = 0
        self.trolleybus_dy = 0
        self.trolleybus_speed = 5  # швидкість руху трамваю
        self.trolleybus_scale = 1.0
        self.trolleybus_scale_speed = 0.01

        # Шрифти та текст
        self.font = pygame.font.SysFont(None, 36)
        self.text_color = (255, 255, 255)
        self.button_font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.text = "Відстеження руху громадського транспорту"
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(self.width // 2, self.height - 50))

        # Кнопки
        self.exit_button_rect = pygame.Rect(10, 10, 100, 50)
        self.next_page_button_rect = pygame.Rect(self.width - 110, 10, 100, 50)
        self.exit_button_text = self.button_font.render("Вихід", True, self.WHITE)
        self.next_page_button_text = self.button_font.render("Далі", True, self.WHITE)

        # Поточна вкладка
        self.current_tab = "ТРАМВАЇ"
        self.routes = self.load_routes("routes.txt")  # Завантаження маршрутів із файлу
        self.selected_route = None  # Вибраний маршрут
        self.show_stops = False  # Прапор для перегляду зупинок
        self.search_text = ""
        self.show_main_screen = True
        self.show_map_screen = False  # Екран для відображення карти
        self.running = True

        # Додаткові налаштування
        self.trolleybus_scale = 1.0
        self.trolleybus_scale_speed = 0.01

    def load_routes(self, filename):
        tram_routes = []
        trolleybus_routes = []
        marshrutka_routes = []

        def open_map_with_route(self, stops):
            # Формуємо URL для Google Maps з усіма зупинками
            base_url = "https://www.google.com/maps/dir/"
            stops_url = "/".join([f"{stop.strip()}" for stop in stops])
            url = f"{base_url}/{stops_url}"


            # Відкриваємо маршрут у веб-браузері
            webbrowser.open(url)

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('Т '):  # Трамваї
                    number, rest = line.split(":")
                    route, stops = rest.split("|")
                    tram_routes.append({"number": number.strip(), "route": route.strip(), "stops": stops.strip().split(',')})
                elif line.startswith('Тр '):  # Тролейбуси
                    number, rest = line.split(":")
                    route, stops = rest.split("|")
                    trolleybus_routes.append({"number": number.strip(), "route": route.strip(), "stops": stops.strip().split(',')})
                elif line.startswith('А '):  # автобуси
                    number, rest = line.split(":")
                    route, stops = rest.split("|")
                    marshrutka_routes.append({"number": number.strip(), "route": route.strip(), "stops": stops.strip().split(',')})

        return {
            "ТРАМВАЇ": tram_routes,
            "ТРОЛЕЙБУСИ": trolleybus_routes,
            "АВТОБУСИ": marshrutka_routes
        }

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            self.update_screen()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.trolleybus_dx = -self.trolleybus_speed
                elif event.key == pygame.K_RIGHT:
                    self.trolleybus_dx = self.trolleybus_speed
                elif event.key == pygame.K_UP:
                    self.trolleybus_dy = -self.trolleybus_speed
                elif event.key == pygame.K_DOWN:
                    self.trolleybus_dy = self.trolleybus_speed

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.trolleybus_dx = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.trolleybus_dy = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Перевірка на натискання кнопок
                if self.exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                if self.next_page_button_rect.collidepoint(event.pos):
                    self.show_main_screen = not self.show_main_screen
                    self.show_stops = False  # Повернення до основного екрана

                if not self.show_main_screen and not self.show_stops:
                    x, y = event.pos
                    # Перевірка натискання на вкладки
                    if 20 <= x <= 120 and 70 <= y <= 100:
                        self.current_tab = "ТРАМВАЇ"
                    elif 140 <= x <= 260 and 70 <= y <= 100:
                        self.current_tab = "ТРОЛЕЙБУСИ"
                    elif 280 <= x <= 400 and 70 <= y <= 100:
                        self.current_tab = "АВТОБУСИ"
                    else:
                        # Перевірка вибору маршруту або кнопки "Відстежити"
                        for i, route in enumerate(self.routes[self.current_tab]):
                            if 20 <= x <= 780 and 120 + i * 50 <= y <= 170 + i * 50:
                                self.selected_route = route
                                self.show_stops = True

                            # Перевірка наявності 'track_button' і обробка кліку
                            if 'track_button' in route and route['track_button'].collidepoint(event.pos):
                                self.show_map_screen = True
                                self.current_tab = "КАРТА"  # Додаємо зміну вкладки на "Карта"
                                self.open_map(self.selected_route['number'], self.selected_route['stops'])

            if event.type == pygame.KEYDOWN:
                # Обробка пошуку
                if event.key == pygame.K_RETURN:
                    # Виконати пошук
                    self.search_routes()
                elif event.key == pygame.K_BACKSPACE:
                    self.search_text = self.search_text[:-1]
                else:
                    self.search_text += event.unicode

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.trolleybus_dx = -self.trolleybus_speed
                elif event.key == pygame.K_RIGHT:
                    self.trolleybus_dx = self.trolleybus_speed
                elif event.key == pygame.K_UP:
                    self.trolleybus_dy = -self.trolleybus_speed
                elif event.key == pygame.K_DOWN:
                    self.trolleybus_dy = self.trolleybus_speed

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.trolleybus_dx = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.trolleybus_dy = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                if self.next_page_button_rect.collidepoint(event.pos):
                    self.show_main_screen = not self.show_main_screen
                    self.show_stops = False  # Повернення до основного екрана

                if not self.show_main_screen and not self.show_stops:
                    x, y = event.pos
                    # Перевірка натискання на вкладки
                    if 20 <= x <= 120 and 70 <= y <= 100:
                        self.current_tab = "ТРАМВАЇ"
                    elif 140 <= x <= 260 and 70 <= y <= 100:
                        self.current_tab = "ТРОЛЕЙБУСИ"
                    elif 280 <= x <= 400 and 70 <= y <= 100:
                        self.current_tab = "АВТОБУСИ"
                    else:
                        # Перевірка вибору маршруту або кнопки "Відстежити"
                        for i, route in enumerate(self.routes[self.current_tab]):
                            if 20 <= x <= 780 and 120 + i * 50 <= y <= 170 + i * 50:
                                self.selected_route = route
                                self.show_stops = True

                            # Перевірка наявності 'track_button' і обробка кліку
                            if 'track_button' in route and route['track_button'].collidepoint(event.pos):
                                self.show_map_screen = True
                                self.current_tab = "КАРТА"  # Додаємо зміну вкладки на "Карта"
                                self.open_map(self.selected_route['number'], self.selected_route['stops'])

            if event.type == pygame.KEYDOWN:
                # Обробка пошуку
                if event.key == pygame.K_RETURN:
                    # Виконати пошук
                    self.search_routes()
                elif event.key == pygame.K_BACKSPACE:
                    self.search_text = self.search_text[:-1]
                else:
                    self.search_text += event.unicode


    def search_routes(self):
        # Реалізація пошуку маршрутів
        pass

    def open_map(self, route_number, stops):
        url = "https://www.google.com/maps"
        webview.create_window('Google Maps', url)
        webview.start()

    def update_screen(self):
        if self.show_map_screen:
            self.render_map_screen()
        elif self.show_stops and self.selected_route:
            self.render_stops()
        else:
            self.render_main()
        self.trolleybus_rect.x += self.trolleybus_dx
        self.trolleybus_rect.y += self.trolleybus_dy

    def render_main(self):
        self.screen.fill(self.WHITE)

        if self.show_main_screen:
            self.screen.fill(self.BLUE)
            self.screen.blit(self.trolleybus_image, self.trolleybus_rect)
            self.screen.blit(self.flag_image, self.flag_rect)
            self.screen.blit(self.text_surface, self.text_rect)
            self.screen.blit(self.exit_button_text, (self.exit_button_rect.x + 10, self.exit_button_rect.y + 10))
            self.screen.blit(self.next_page_button_text, (self.next_page_button_rect.x + 10, self.next_page_button_rect.y + 10))
        else:
            pygame.draw.rect(self.screen, self.LIGHT_GRAY, (10, 10, self.width - 20, 40))
            search_text_surface = self.small_font.render(self.search_text, True, self.DARK_GRAY)
            self.screen.blit(search_text_surface, (20, 20))

            tram_text_surface = self.small_font.render("ТРАМВАЇ", True, self.BLUE if self.current_tab == "ТРАМВАЇ" else self.DARK_GRAY)
            self.screen.blit(tram_text_surface, (20, 70))

            trolley_text_surface = self.small_font.render("ТРОЛЕЙБУСИ", True, self.BLUE if self.current_tab == "ТРОЛЕЙБУСИ" else self.DARK_GRAY)
            self.screen.blit(trolley_text_surface, (140, 70))

            marshrutka_text_surface = self.small_font.render("МАРШРУТКИ", True, self.BLUE if self.current_tab == "МАРШРУТКИ" else self.DARK_GRAY)
            self.screen.blit(marshrutka_text_surface, (280, 70))

            start_y = 120
            for i, route in enumerate(self.routes[self.current_tab]):
                if self.search_text.lower() in route['number'].lower() or self.search_text.lower() in route['route'].lower():
                    route_text_surface = self.small_font.render(f"{route['number']} - {route['route']}", True, self.BLACK)
                    self.screen.blit(route_text_surface, (20, start_y))

                    # Створення кнопки "Відстежити"
                    track_button_surface = self.small_font.render("Відстежити", True, self.BLUE)
                    track_button_rect = track_button_surface.get_rect(topleft=(650, start_y))
                    self.screen.blit(track_button_surface, track_button_rect.topleft)
                    route['track_button'] = track_button_rect

                    start_y += 50

    def render_stops(self):
        self.screen.fill(self.WHITE)
        title_surface = self.font.render(f"Зупинки маршруту {self.selected_route['number']}", True, self.BLACK)
        self.screen.blit(title_surface, (20, 20))

        start_y = 100
        for stop in self.selected_route["stops"]:
            stop_surface = self.small_font.render(stop, True, self.BLACK)
            self.screen.blit(stop_surface, (20, start_y))
            start_y += 30

    def render_map_screen(self):
        self.screen.fill(self.WHITE)
        map_text_surface = self.font.render("Карта маршруту", True, self.BLACK)
        self.screen.blit(map_text_surface, (self.width // 2 - 100, 50))
        back_button_surface = self.button_font.render("Назад", True, self.WHITE)
        back_button_rect = pygame.Rect(10, 10, 100, 50)
        pygame.draw.rect(self.screen, self.DARK_GRAY, back_button_rect)
        self.screen.blit(back_button_surface, (back_button_rect.x + 10, back_button_rect.y + 10))


    # Запуск додатку
app = TransportApp()
app.run()
