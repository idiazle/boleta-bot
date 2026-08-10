# Bot Extractor de Boletas

Bot que utiliza visión artificial para extraer datos de boletas/facturas electrónicas usando la API de MiniMax (modelo MiniMax-M3).

## Datos Extraídos

- `ruc` - RUC del emisor
- `razon_social` - Nombre de la empresa
- `fecha` - Fecha de la boleta
- `monto_total` - Monto total
- `igv` - Impuesto General a las Ventas

## Requisitos

- Python 3.8+
- Cuenta en [MiniMax](https://platform.minimaxi.com) con API key

## Instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repo>
cd telegram-bot
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env y colocar tu API_KEY_MINIMAX
```

## Uso

1. Coloca la imagen de la boleta en la carpeta `bot-boletas/`
2. Edita la variable `RUTA_IMAGEN` en `main.py` con el nombre de tu imagen
3. Ejecuta:
```bash
python main.py
```

Los resultados se guardan en la carpeta `output/` con nombres únicos (evita sobreescritura).

## Estructura del Proyecto

```
telegram-bot/
├── bot-boletas/       # Imágenes de boletas de entrada
├── output/            # Resultados JSON extraídos
├── main.py            # Script principal
├── requirements.txt    # Dependencias Python
├── .env               # Variables de entorno (no commits)
├── .env.example       # Plantilla de .env
└── README.md
```

## API Utilizada

- **MiniMax Vision API** - Modelo `MiniMax-M3`
- Endpoint: `https://api.minimax.io/v1/text/chatcompletion_v2`
- Documentación: [MiniMax Platform](https://platform.minimaxi.com/docs)
