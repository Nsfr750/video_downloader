"""Translation strings for Video Downloader application.

This module contains all translation strings for supported languages.
"""

TRANSLATIONS = {
    'en': {
        'app_name': 'Video Downloader',
        'app_title': 'Video Downloader - Download videos from the internet',
        'menu_title': 'Main Menu',
        'menu_download': 'Download Videos',
        'menu_settings': 'Settings',
        'menu_help': 'Help',
        'menu_about': 'About',
        'menu_exit': 'Exit',
        'menu_view_logs': 'View Logs',
        'menu_language': 'Language',
        'menu_update': 'Check for Updates',
        'enter_urls': 'Enter video URLs (one per line, empty line to finish):',
        'downloading': 'Downloading: {url}',
        'download_complete': 'Download complete: {url}',
        'download_failed': 'Download failed: {url} - {error}',
        'download_progress': 'Download progress: {percent:.1f}%',
        'no_urls': 'No URLs provided.',
        'invalid_url': 'Invalid URL: {url}',
        'quality_title': 'Quality Selection',
        'quality_select': 'Select video quality:',
        'quality_best': 'Best (best available)',
        'quality_worst': 'Worst (lowest quality)',
        'quality_1080p': '1080p',
        'quality_720p': '720p',
        'quality_480p': '480p',
        'quality_360p': '360p',
        'quality_audio': 'Audio only',
        'quality_default': 'Enter your choice (1-7, default: 1):',
        'quality_invalid': 'Invalid choice. Please enter a number between 1 and 7.',
        'quality_1080p_label': '1080p',
        'quality_720p_label': '720p',
        'quality_480p_label': '480p',
        'quality_360p_label': '360p',
        'format_title': 'Format Selection',
        'format_select': 'Select output format:',
        'format_auto': 'Auto (keep original)',
        'format_default': 'Enter your choice (1-8, default: 1):',
        'format_invalid': 'Invalid choice. Please enter a number between 1 and 8.',
        'format_mp4': 'MP4',
        'format_webm': 'WebM',
        'format_mkv': 'MKV',
        'format_avi': 'AVI',
        'format_mp3': 'MP3 (audio)',
        'format_m4a': 'M4A (audio)',
        'format_wav': 'WAV (audio)',
        'paypal_label': 'PayPal:',
        'monero_label': 'Monero (XMR):',
        'qr_error_load': 'Could not load QR code',
        'qr_error_generate': 'Error generating QR code: {error}',
        'qr_unavailable': '(QR code not available: qrcode or ImageMagick missing)',
        'settings_title': 'Settings',
        'settings_language': 'Current language: {lang}',
        'settings_download_dir': 'Download directory: {dir}',
        'settings_format': 'Preferred format: {format}',
        'help_title': 'Help',
        'help_content': '''
Video Downloader Help

1. Download Videos:
   - Add one or more video URLs (CLI: one per line, empty line to start)
   - Choose the download directory (default: downloads)
   - Supported platforms: YouTube, Vimeo, and many more

2. Quality and Format:
   - Quality: best, worst, 1080p, 720p, 480p, 360p or audio only
   - Format: auto keeps the original format, or choose
     mp4, webm, mkv, avi, mp3, m4a, wav

3. Playlists:
   - Enable the playlist option to download every video of a playlist
   - Videos are saved in a folder named after the playlist and numbered
   - With the option disabled, a playlist URL downloads a single video

4. Download History:
   - Lists completed and failed downloads with date, quality and format
   - The history can be cleared

5. Logs:
   - View application logs
   - Clear logs

6. Language:
   - Switch between English, Italian, Spanish, French and German

7. Update:
   - Check for application updates

8. Sponsor:
   - Support the project with PayPal or Monero (QR code)
        ''',
        'about_title': 'About',
        'about_content': '''
Video Downloader v{}

A Python application for downloading videos from the internet using yt-dlp.

© Copyright 2024-2026 Tuxxle - All rights reserved.

Author: Nsfr750
Website: https://www.tuxxle.org
Email: nsfr750@yandex.com
GitHub: https://github.com/Nsfr750

Organization: Tuxxle
License: GPLv3
        ''',
        'sponsor_title': 'Sponsor',
        'sponsor_content': '''
Support the development of Video Downloader

PayPal: https://paypal.me/3dmega

Monero: See QR code in the sponsor dialog

Thank you for your support!
        ''',
        'language_title': 'Language Selection',
        'language_select': 'Select language:',
        'language_changed': 'Language changed to {}',
        'update_title': 'Update',
        'update_checking': 'Checking for updates...',
        'update_available': 'Update available: {}',
        'update_latest': 'You are using the latest version: {}',
        'update_error': 'Error checking for updates: {}',
        'log_title': 'Log Viewer',
        'log_no_files': 'No log files found.',
        'back': 'Back',
        'close': 'Close',
        'yes': 'Yes',
        'no': 'No',
        'confirm': 'Confirm',
        'cancel': 'Cancel',
        'error': 'Error',
        'success': 'Success',
        'warning': 'Warning',
        'info': 'Information',
        'enter_your_choice': 'Enter your choice:',
        'invalid_choice': 'Invalid choice. Please try again.',
        'press_enter_continue': 'Press Enter to continue...',
        'ui_url_placeholder': 'Enter video URL here...',
        'ui_add_url': 'Add URL',
        'ui_clear_urls': 'Clear URLs',
        'ui_download': 'Download',
        'ui_downloading': 'Downloading...',
        'ui_progress': 'Progress: {percent:.1f}%',
        'ui_complete': 'Complete',
        'ui_failed': 'Failed',
        'ui_status': 'Status',
        'ui_url_list': 'URL List',
        'ui_download_dir': 'Download Directory:',
        'ui_browse': 'Browse',
        'ui_select_dir': 'Select Download Directory',
        'ui_log_viewer': 'Log Viewer',
        'ui_refresh_logs': 'Refresh',
        'ui_clear_logs': 'Clear Logs',
        'ui_language': 'Language:',
        'ui_sponsor': 'Sponsor',
        'ui_check_updates': 'Check for Updates',
        'ui_no_urls_added': 'No URLs added yet.',
        'ui_download_started': 'Download started for {count} URL(s)',
        'ui_download_finished': 'Download finished',
        'ui_download_summary': 'Download Summary',
        'ui_successful': 'Successful: {count}',
        'ui_failed_count': 'Failed: {count}',
        'url_list': 'URL List',
        'menu_history': 'Download History',
        'playlist_question': 'Download entire playlists?',
        'yes_no_hint': ' (y/N): ',
        'ui_playlist': 'Download entire playlist (when the URL is a playlist)',
        'history_empty': 'No downloads in history.',
        'history_clear': 'Clear History',
        'history_clear_confirm': 'Delete the whole download history?',
        'history_cleared': 'History cleared.',
        'history_col_date': 'Date',
        'history_col_title': 'Title',
        'history_col_status': 'Status',
        'history_col_quality': 'Quality',
        'history_col_format': 'Format',
        'history_col_url': 'URL',
        'history_status_completed': 'Completed',
        'history_status_failed': 'Failed',
    },
    'it': {
        'app_name': 'Video Downloader',
        'app_title': 'Video Downloader - Scarica video da internet',
        'menu_title': 'Menu Principale',
        'menu_download': 'Scarica Video',
        'menu_settings': 'Impostazioni',
        'menu_help': 'Aiuto',
        'menu_about': 'Informazioni',
        'menu_exit': 'Esci',
        'menu_view_logs': 'Visualizza Log',
        'menu_language': 'Lingua',
        'menu_update': 'Controlla Aggiornamenti',
        'enter_urls': 'Inserisci URL video (uno per riga, riga vuota per finire):',
        'downloading': 'Scaricamento: {url}',
        'download_complete': 'Scaricamento completato: {url}',
        'download_failed': 'Scaricamento fallito: {url} - {error}',
        'download_progress': 'Progresso scaricamento: {percent:.1f}%',
        'no_urls': 'Nessun URL fornito.',
        'invalid_url': 'URL non valido: {url}',
        'quality_title': 'Selezione Qualità',
        'quality_select': 'Seleziona qualità video:',
        'quality_best': 'Migliore (disponibile)',
        'quality_worst': 'Peggiore (bassa qualità)',
        'quality_1080p': '1080p',
        'quality_720p': '720p',
        'quality_480p': '480p',
        'quality_360p': '360p',
        'quality_audio': 'Solo audio',
        'quality_default': 'Inserisci la tua scelta (1-7, default: 1):',
        'quality_invalid': 'Scelta non valida. Inserisci un numero tra 1 e 7.',
        'quality_1080p_label': '1080p',
        'quality_720p_label': '720p',
        'quality_480p_label': '480p',
        'quality_360p_label': '360p',
        'format_title': 'Selezione Formato',
        'format_select': 'Seleziona formato di output:',
        'format_auto': 'Auto (mantieni originale)',
        'format_default': 'Inserisci la tua scelta (1-8, default: 1):',
        'format_invalid': 'Scelta non valida. Inserisci un numero tra 1 e 8.',
        'format_mp4': 'MP4',
        'format_webm': 'WebM',
        'format_mkv': 'MKV',
        'format_avi': 'AVI',
        'format_mp3': 'MP3 (audio)',
        'format_m4a': 'M4A (audio)',
        'format_wav': 'WAV (audio)',
        'paypal_label': 'PayPal:',
        'monero_label': 'Monero (XMR):',
        'qr_error_load': 'Impossibile caricare il codice QR',
        'qr_error_generate': 'Errore nella generazione del codice QR: {error}',
        'qr_unavailable': '(Codice QR non disponibile: qrcode o ImageMagick mancante)',
        'settings_title': 'Impostazioni',
        'settings_language': 'Lingua attuale: {lang}',
        'settings_download_dir': 'Directory di download: {dir}',
        'settings_format': 'Formato preferito: {format}',
        'help_title': 'Aiuto',
        'help_content': '''
Aiuto Video Downloader

1. Scarica Video:
   - Aggiungi uno o più URL video (CLI: uno per riga, riga vuota per iniziare)
   - Scegli la directory di download (predefinita: downloads)
   - Piattaforme supportate: YouTube, Vimeo e molte altre

2. Qualità e Formato:
   - Qualità: migliore, peggiore, 1080p, 720p, 480p, 360p o solo audio
   - Formato: auto mantiene il formato originale, oppure scegli
     mp4, webm, mkv, avi, mp3, m4a, wav

3. Playlist:
   - Attiva l'opzione playlist per scaricare tutti i video di una playlist
   - I video vengono salvati in una cartella con il nome della playlist e numerati
   - Con l'opzione disattivata, un URL di playlist scarica un solo video

4. Cronologia Download:
   - Elenca i download completati e falliti con data, qualità e formato
   - La cronologia può essere cancellata

5. Log:
   - Visualizza log dell'applicazione
   - Cancella log

6. Lingua:
   - Cambia tra inglese, italiano, spagnolo, francese e tedesco

7. Aggiornamenti:
   - Controlla aggiornamenti dell'applicazione

8. Sponsor:
   - Supporta il progetto con PayPal o Monero (codice QR)
        ''',
        'about_title': 'Informazioni',
        'about_content': '''
Video Downloader v{}

Un\'applicazione Python per scaricare video da internet usando yt-dlp.

© Copyright 2024-2026 Tuxxle - Tutti i diritti riservati.

Autore: Nsfr750
Sito web: https://www.tuxxle.org
Email: nsfr750@yandex.com
GitHub: https://github.com/Nsfr750py clean_pycache.py

Organizzazione: Tuxxle
Licenza: GPLv3
        ''',
        'sponsor_title': 'Sponsor',
        'sponsor_content': '''
Supporta lo sviluppo di Video Downloader

PayPal: https://paypal.me/3dmega

Monero: Vedi il codice QR nella finestra sponsor

Grazie per il tuo supporto!
        ''',
        'language_title': 'Selezione Lingua',
        'language_select': 'Seleziona lingua:',
        'language_changed': 'Lingua cambiata in {}',
        'update_title': 'Aggiornamento',
        'update_checking': 'Controllo aggiornamenti...',
        'update_available': 'Aggiornamento disponibile: {}',
        'update_latest': 'Stai usando l\'ultima versione: {}',
        'update_error': 'Errore nel controllo aggiornamenti: {}',
        'log_title': 'Visualizzatore Log',
        'log_no_files': 'Nessun file log trovato.',
        'back': 'Indietro',
        'close': 'Chiudi',
        'yes': 'Sì',
        'no': 'No',
        'confirm': 'Conferma',
        'cancel': 'Annulla',
        'error': 'Errore',
        'success': 'Successo',
        'warning': 'Avviso',
        'info': 'Informazione',
        'enter_your_choice': 'Inserisci la tua scelta:',
        'invalid_choice': 'Scelta non valida. Riprova.',
        'press_enter_continue': 'Premi Invio per continuare...',
        'ui_url_placeholder': 'Inserisci URL video qui...',
        'ui_add_url': 'Aggiungi URL',
        'ui_clear_urls': 'Cancella URL',
        'ui_download': 'Scarica',
        'ui_downloading': 'Scaricamento...',
        'ui_progress': 'Progresso: {percent:.1f}%',
        'ui_complete': 'Completato',
        'ui_failed': 'Fallito',
        'ui_status': 'Stato',
        'ui_url_list': 'Lista URL',
        'ui_download_dir': 'Directory Download:',
        'ui_browse': 'Sfoglia',
        'ui_select_dir': 'Seleziona Directory Download',
        'ui_log_viewer': 'Visualizzatore Log',
        'ui_refresh_logs': 'Aggiorna',
        'ui_clear_logs': 'Cancella Log',
        'ui_language': 'Lingua:',
        'ui_sponsor': 'Sponsor',
        'ui_check_updates': 'Controlla Aggiornamenti',
        'ui_no_urls_added': 'Nessun URL aggiunto.',
        'ui_download_started': 'Download avviato per {count} URL',
        'ui_download_finished': 'Download completato',
        'ui_download_summary': 'Riepilogo Download',
        'ui_successful': 'Riusciti: {count}',
        'ui_failed_count': 'Falliti: {count}',
        'url_list': 'Lista URL',
        'menu_history': 'Cronologia Download',
        'playlist_question': 'Scaricare le playlist intere?',
        'yes_no_hint': ' (s/N): ',
        'ui_playlist': "Scarica l'intera playlist (se l'URL è una playlist)",
        'history_empty': 'Nessun download nella cronologia.',
        'history_clear': 'Cancella Cronologia',
        'history_clear_confirm': "Eliminare l'intera cronologia dei download?",
        'history_cleared': 'Cronologia cancellata.',
        'history_col_date': 'Data',
        'history_col_title': 'Titolo',
        'history_col_status': 'Stato',
        'history_col_quality': 'Qualità',
        'history_col_format': 'Formato',
        'history_col_url': 'URL',
        'history_status_completed': 'Completato',
        'history_status_failed': 'Fallito',
    },
    'es': {
        'app_name': 'Video Downloader',
        'app_title': 'Video Downloader - Descarga videos de internet',
        'menu_title': 'Menú Principal',
        'menu_download': 'Descargar Videos',
        'menu_settings': 'Configuración',
        'menu_help': 'Ayuda',
        'menu_about': 'Acerca de',
        'menu_exit': 'Salir',
        'menu_view_logs': 'Ver Registros',
        'menu_language': 'Idioma',
        'menu_update': 'Buscar Actualizaciones',
        'enter_urls': 'Ingrese URLs de videos (uno por línea, línea vacía para terminar):',
        'downloading': 'Descargando: {url}',
        'download_complete': 'Descarga completada: {url}',
        'download_failed': 'Descarga fallida: {url} - {error}',
        'download_progress': 'Progreso de descarga: {percent:.1f}%',
        'no_urls': 'No se proporcionaron URLs.',
        'invalid_url': 'URL inválido: {url}',
        'quality_title': 'Selección de Calidad',
        'quality_select': 'Seleccionar calidad de video:',
        'quality_best': 'Mejor (disponible)',
        'quality_worst': 'Peor (baja calidad)',
        'quality_1080p': '1080p',
        'quality_720p': '720p',
        'quality_480p': '480p',
        'quality_360p': '360p',
        'quality_audio': 'Solo audio',
        'quality_default': 'Ingrese su elección (1-7, default: 1):',
        'quality_invalid': 'Elección inválida. Ingrese un número entre 1 y 7.',
        'quality_1080p_label': '1080p',
        'quality_720p_label': '720p',
        'quality_480p_label': '480p',
        'quality_360p_label': '360p',
        'format_title': 'Selección de Formato',
        'format_select': 'Seleccionar formato de salida:',
        'format_auto': 'Auto (mantener original)',
        'format_default': 'Ingrese su elección (1-8, default: 1):',
        'format_invalid': 'Elección inválida. Ingrese un número entre 1 y 8.',
        'format_mp4': 'MP4',
        'format_webm': 'WebM',
        'format_mkv': 'MKV',
        'format_avi': 'AVI',
        'format_mp3': 'MP3 (audio)',
        'format_m4a': 'M4A (audio)',
        'format_wav': 'WAV (audio)',
        'paypal_label': 'PayPal:',
        'monero_label': 'Monero (XMR):',
        'qr_error_load': 'No se pudo cargar el código QR',
        'qr_error_generate': 'Error al generar el código QR: {error}',
        'qr_unavailable': '(Código QR no disponible: falta qrcode o ImageMagick)',
        'settings_title': 'Configuración',
        'settings_language': 'Idioma actual: {lang}',
        'settings_download_dir': 'Directorio de descarga: {dir}',
        'settings_format': 'Formato preferido: {format}',
        'help_title': 'Ayuda',
        'help_content': '''
Ayuda de Video Downloader

1. Descargar Videos:
   - Agregue uno o más URLs de videos (CLI: uno por línea, línea vacía para comenzar)
   - Elija el directorio de descarga (predeterminado: downloads)
   - Plataformas soportadas: YouTube, Vimeo y muchas más

2. Calidad y Formato:
   - Calidad: mejor, peor, 1080p, 720p, 480p, 360p o solo audio
   - Formato: auto mantiene el formato original, o elija
     mp4, webm, mkv, avi, mp3, m4a, wav

3. Listas de reproducción:
   - Active la opción de lista para descargar todos los videos de una lista
   - Los videos se guardan en una carpeta con el nombre de la lista y numerados
   - Con la opción desactivada, una URL de lista descarga un solo video

4. Historial de Descargas:
   - Muestra las descargas completadas y fallidas con fecha, calidad y formato
   - El historial se puede borrar

5. Registros:
   - Ver registros de la aplicación
   - Limpiar registros

6. Idioma:
   - Cambiar entre inglés, italiano, español, francés y alemán

7. Actualización:
   - Buscar actualizaciones de la aplicación

8. Patrocinador:
   - Apoye el proyecto con PayPal o Monero (código QR)
        ''',
        'about_title': 'Acerca de',
        'about_content': '''
Video Downloader v{}

Una aplicación Python para descargar videos de internet usando yt-dlp.

© Copyright 2024-2026 Tuxxle - Todos los derechos reservados.

Autor: Nsfr750
Sitio web: https://www.tuxxle.org
Email: nsfr750@yandex.com
GitHub: https://github.com/Nsfr750

Organización: Tuxxle
Licencia: GPLv3
        ''',
        'sponsor_title': 'Patrocinador',
        'sponsor_content': '''
Apoya el desarrollo de Video Downloader

PayPal: https://paypal.me/3dmega

Monero: Ver el código QR en el diálogo de patrocinador

¡Gracias por tu apoyo!
        ''',
        'language_title': 'Selección de Idioma',
        'language_select': 'Seleccionar idioma:',
        'language_changed': 'Idioma cambiado a {}',
        'update_title': 'Actualización',
        'update_checking': 'Buscando actualizaciones...',
        'update_available': 'Actualización disponible: {}',
        'update_latest': 'Estás usando la última versión: {}',
        'update_error': 'Error al buscar actualizaciones: {}',
        'log_title': 'Visor de Registros',
        'log_no_files': 'No se encontraron archivos de registro.',
        'back': 'Atrás',
        'close': 'Cerrar',
        'yes': 'Sí',
        'no': 'No',
        'confirm': 'Confirmar',
        'cancel': 'Cancelar',
        'error': 'Error',
        'success': 'Éxito',
        'warning': 'Advertencia',
        'info': 'Información',
        'enter_your_choice': 'Ingrese su elección:',
        'invalid_choice': 'Elección inválida. Intente de nuevo.',
        'press_enter_continue': 'Presione Enter para continuar...',
        'ui_url_placeholder': 'Ingrese URL de video aquí...',
        'ui_add_url': 'Agregar URL',
        'ui_clear_urls': 'Limpiar URLs',
        'ui_download': 'Descargar',
        'ui_downloading': 'Descargando...',
        'ui_progress': 'Progreso: {percent:.1f}%',
        'ui_complete': 'Completo',
        'ui_failed': 'Fallido',
        'ui_status': 'Estado',
        'ui_url_list': 'Lista de URLs',
        'ui_download_dir': 'Directorio de Descarga:',
        'ui_browse': 'Explorar',
        'ui_select_dir': 'Seleccionar Directorio de Descarga',
        'ui_log_viewer': 'Visor de Registros',
        'ui_refresh_logs': 'Actualizar',
        'ui_clear_logs': 'Limpiar Registros',
        'ui_language': 'Idioma:',
        'ui_sponsor': 'Patrocinador',
        'ui_check_updates': 'Buscar Actualizaciones',
        'ui_no_urls_added': 'No se han agregado URLs.',
        'ui_download_started': 'Descarga iniciada para {count} URL(s)',
        'ui_download_finished': 'Descarga finalizada',
        'ui_download_summary': 'Resumen de Descarga',
        'ui_successful': 'Exitosos: {count}',
        'ui_failed_count': 'Fallidos: {count}',
        'url_list': 'Lista de URLs',
        'menu_history': 'Historial de Descargas',
        'playlist_question': '¿Descargar las listas de reproducción completas?',
        'yes_no_hint': ' (s/N): ',
        'ui_playlist': 'Descargar la lista de reproducción completa (si la URL es una lista)',
        'history_empty': 'No hay descargas en el historial.',
        'history_clear': 'Borrar Historial',
        'history_clear_confirm': '¿Eliminar todo el historial de descargas?',
        'history_cleared': 'Historial borrado.',
        'history_col_date': 'Fecha',
        'history_col_title': 'Título',
        'history_col_status': 'Estado',
        'history_col_quality': 'Calidad',
        'history_col_format': 'Formato',
        'history_col_url': 'URL',
        'history_status_completed': 'Completado',
        'history_status_failed': 'Fallido',
    },
    'fr': {
        'app_name': 'Video Downloader',
        'app_title': 'Video Downloader - Télécharger des vidéos d\'internet',
        'menu_title': 'Menu Principal',
        'menu_download': 'Télécharger Videos',
        'menu_settings': 'Paramètres',
        'menu_help': 'Aide',
        'menu_about': 'À propos',
        'menu_exit': 'Quitter',
        'menu_view_logs': 'Voir les Journaux',
        'menu_language': 'Langue',
        'menu_update': 'Vérifier les Mises à jour',
        'enter_urls': 'Entrez les URLs des vidéos (une par ligne, ligne vide pour terminer):',
        'downloading': 'Téléchargement: {url}',
        'download_complete': 'Téléchargement terminé: {url}',
        'download_failed': 'Téléchargement échoué: {url} - {error}',
        'download_progress': 'Progression du téléchargement: {percent:.1f}%',
        'no_urls': 'Aucune URL fournie.',
        'invalid_url': 'URL invalide: {url}',
        'quality_title': 'Sélection de Qualité',
        'quality_select': 'Sélectionner la qualité vidéo:',
        'quality_best': 'Meilleure (disponible)',
        'quality_worst': 'Pire (basse qualité)',
        'quality_1080p': '1080p',
        'quality_720p': '720p',
        'quality_480p': '480p',
        'quality_360p': '360p',
        'quality_audio': 'Audio uniquement',
        'quality_default': 'Entrez votre choix (1-7, défaut: 1):',
        'quality_invalid': 'Choix invalide. Entrez un nombre entre 1 et 7.',
        'quality_1080p_label': '1080p',
        'quality_720p_label': '720p',
        'quality_480p_label': '480p',
        'quality_360p_label': '360p',
        'format_title': 'Sélection de Format',
        'format_select': 'Sélectionner le format de sortie:',
        'format_auto': 'Auto (garder l\'original)',
        'format_default': 'Entrez votre choix (1-8, défaut: 1):',
        'format_invalid': 'Choix invalide. Entrez un nombre entre 1 et 8.',
        'format_mp4': 'MP4',
        'format_webm': 'WebM',
        'format_mkv': 'MKV',
        'format_avi': 'AVI',
        'format_mp3': 'MP3 (audio)',
        'format_m4a': 'M4A (audio)',
        'format_wav': 'WAV (audio)',
        'paypal_label': 'PayPal:',
        'monero_label': 'Monero (XMR):',
        'qr_error_load': 'Impossible de charger le code QR',
        'qr_error_generate': 'Erreur lors de la génération du code QR: {error}',
        'qr_unavailable': '(Code QR non disponible : qrcode ou ImageMagick manquant)',
        'settings_title': 'Paramètres',
        'settings_language': 'Langue actuelle: {lang}',
        'settings_download_dir': 'Répertoire de téléchargement: {dir}',
        'settings_format': 'Format préféré: {format}',
        'help_title': 'Aide',
        'help_content': '''
Aide Video Downloader

1. Télécharger Videos:
   - Ajoutez une ou plusieurs URLs de vidéos (CLI: une par ligne, ligne vide pour commencer)
   - Choisissez le répertoire de téléchargement (par défaut: downloads)
   - Plateformes supportées: YouTube, Vimeo et bien d'autres

2. Qualité et Format:
   - Qualité: meilleure, pire, 1080p, 720p, 480p, 360p ou audio uniquement
   - Format: auto garde le format original, ou choisissez
     mp4, webm, mkv, avi, mp3, m4a, wav

3. Playlists:
   - Activez l'option playlist pour télécharger toutes les vidéos d'une playlist
   - Les vidéos sont enregistrées dans un dossier au nom de la playlist et numérotées
   - Avec l'option désactivée, une URL de playlist télécharge une seule vidéo

4. Historique des Téléchargements:
   - Liste les téléchargements terminés et échoués avec date, qualité et format
   - L'historique peut être effacé

5. Journaux:
   - Voir les journaux de l'application
   - Effacer les journaux

6. Langue:
   - Changer entre anglais, italien, espagnol, français et allemand

7. Mise à jour:
   - Vérifier les mises à jour de l'application

8. Sponsor:
   - Soutenez le projet avec PayPal ou Monero (code QR)
        ''',
        'about_title': 'À propos',
        'about_content': '''
Video Downloader v{}

Une application Python pour télécharger des vidéos d\'internet en utilisant yt-dlp.

© Copyright 2024-2026 Tuxxle - Tous droits réservés.

Auteur: Nsfr750
Site web: https://www.tuxxle.org
Email: nsfr750@yandex.com
GitHub: https://github.com/Nsfr750

Organisation: Tuxxle
Licence: GPLv3
        ''',
        'sponsor_title': 'Sponsor',
        'sponsor_content': '''
Soutenez le développement de Video Downloader

PayPal: https://paypal.me/3dmega

Monero: Voir le code QR dans la boîte de dialogue sponsor

Merci pour votre soutien!
        ''',
        'language_title': 'Sélection de Langue',
        'language_select': 'Sélectionner la langue:',
        'language_changed': 'Langue changée en {}',
        'update_title': 'Mise à jour',
        'update_checking': 'Vérification des mises à jour...',
        'update_available': 'Mise à jour disponible: {}',
        'update_latest': 'Vous utilisez la dernière version: {}',
        'update_error': 'Erreur lors de la vérification des mises à jour: {}',
        'log_title': 'Visionneuse de Journaux',
        'log_no_files': 'Aucun fichier journal trouvé.',
        'back': 'Retour',
        'close': 'Fermer',
        'yes': 'Oui',
        'no': 'Non',
        'confirm': 'Confirmer',
        'cancel': 'Annuler',
        'error': 'Erreur',
        'success': 'Succès',
        'warning': 'Avertissement',
        'info': 'Information',
        'enter_your_choice': 'Entrez votre choix:',
        'invalid_choice': 'Choix invalide. Veuillez réessayer.',
        'press_enter_continue': 'Appuyez sur Entrée pour continuer...',
        'ui_url_placeholder': 'Entrez l\'URL vidéo ici...',
        'ui_add_url': 'Ajouter URL',
        'ui_clear_urls': 'Effacer URLs',
        'ui_download': 'Télécharger',
        'ui_downloading': 'Téléchargement...',
        'ui_progress': 'Progression: {percent:.1f}%',
        'ui_complete': 'Terminé',
        'ui_failed': 'Échoué',
        'ui_status': 'Statut',
        'ui_url_list': 'Liste URLs',
        'ui_download_dir': 'Répertoire de Téléchargement:',
        'ui_browse': 'Parcourir',
        'ui_select_dir': 'Sélectionner Répertoire de Téléchargement',
        'ui_log_viewer': 'Visionneuse de Journaux',
        'ui_refresh_logs': 'Actualiser',
        'ui_clear_logs': 'Effacer Journaux',
        'ui_language': 'Langue:',
        'ui_sponsor': 'Sponsor',
        'ui_check_updates': 'Vérifier Mises à jour',
        'ui_no_urls_added': 'Aucune URL ajoutée.',
        'ui_download_started': 'Téléchargement démarré pour {count} URL(s)',
        'ui_download_finished': 'Téléchargement terminé',
        'ui_download_summary': 'Résumé du Téléchargement',
        'ui_successful': 'Réussis: {count}',
        'ui_failed_count': 'Échoués: {count}',
        'url_list': 'Liste URLs',
        'menu_history': 'Historique des Téléchargements',
        'playlist_question': 'Télécharger les playlists entières ?',
        'yes_no_hint': ' (o/N) : ',
        'ui_playlist': "Télécharger toute la playlist (si l'URL est une playlist)",
        'history_empty': "Aucun téléchargement dans l'historique.",
        'history_clear': "Effacer l'Historique",
        'history_clear_confirm': "Supprimer tout l'historique des téléchargements ?",
        'history_cleared': 'Historique effacé.',
        'history_col_date': 'Date',
        'history_col_title': 'Titre',
        'history_col_status': 'Statut',
        'history_col_quality': 'Qualité',
        'history_col_format': 'Format',
        'history_col_url': 'URL',
        'history_status_completed': 'Terminé',
        'history_status_failed': 'Échoué',
    },
    'de': {
        'app_name': 'Video Downloader',
        'app_title': 'Video Downloader - Videos aus dem Internet herunterladen',
        'menu_title': 'Hauptmenü',
        'menu_download': 'Videos Herunterladen',
        'menu_settings': 'Einstellungen',
        'menu_help': 'Hilfe',
        'menu_about': 'Über',
        'menu_exit': 'Beenden',
        'menu_view_logs': 'Protokolle Anzeigen',
        'menu_language': 'Sprache',
        'menu_update': 'Nach Updates Suchen',
        'enter_urls': 'Video-URLs eingeben (eine pro Zeile, leere Zeile zum Beenden):',
        'downloading': 'Herunterladen: {url}',
        'download_complete': 'Download abgeschlossen: {url}',
        'download_failed': 'Download fehlgeschlagen: {url} - {error}',
        'download_progress': 'Download-Fortschritt: {percent:.1f}%',
        'no_urls': 'Keine URLs angegeben.',
        'invalid_url': 'Ungültige URL: {url}',
        'quality_title': 'Qualitätsauswahl',
        'quality_select': 'Videoqualität auswählen:',
        'quality_best': 'Beste (verfügbar)',
        'quality_worst': 'Schlechteste (niedrige Qualität)',
        'quality_1080p': '1080p',
        'quality_720p': '720p',
        'quality_480p': '480p',
        'quality_360p': '360p',
        'quality_audio': 'Nur Audio',
        'quality_default': 'Geben Sie Ihre Wahl ein (1-7, Standard: 1):',
        'quality_invalid': 'Ungültige Wahl. Geben Sie eine Zahl zwischen 1 und 7 ein.',
        'quality_1080p_label': '1080p',
        'quality_720p_label': '720p',
        'quality_480p_label': '480p',
        'quality_360p_label': '360p',
        'format_title': 'Formatauswahl',
        'format_select': 'Ausgabeformat auswählen:',
        'format_auto': 'Auto (original beibehalten)',
        'format_default': 'Geben Sie Ihre Wahl ein (1-8, Standard: 1):',
        'format_invalid': 'Ungültige Wahl. Geben Sie eine Zahl zwischen 1 und 8 ein.',
        'format_mp4': 'MP4',
        'format_webm': 'WebM',
        'format_mkv': 'MKV',
        'format_avi': 'AVI',
        'format_mp3': 'MP3 (Audio)',
        'format_m4a': 'M4A (Audio)',
        'format_wav': 'WAV (Audio)',
        'paypal_label': 'PayPal:',
        'monero_label': 'Monero (XMR):',
        'qr_error_load': 'QR-Code konnte nicht geladen werden',
        'qr_error_generate': 'Fehler beim Generieren des QR-Codes: {error}',
        'qr_unavailable': '(QR-Code nicht verfügbar: qrcode oder ImageMagick fehlt)',
        'settings_title': 'Einstellungen',
        'settings_language': 'Aktuelle Sprache: {lang}',
        'settings_download_dir': 'Download-Verzeichnis: {dir}',
        'settings_format': 'Bevorzugtes Format: {format}',
        'help_title': 'Hilfe',
        'help_content': '''
Video Downloader Hilfe

1. Videos Herunterladen:
   - Fügen Sie eine oder mehrere Video-URLs hinzu (CLI: eine pro Zeile, leere Zeile zum Starten)
   - Wählen Sie das Download-Verzeichnis (Standard: downloads)
   - Unterstützte Plattformen: YouTube, Vimeo und viele mehr

2. Qualität und Format:
   - Qualität: beste, schlechteste, 1080p, 720p, 480p, 360p oder nur Audio
   - Format: Auto behält das Originalformat bei, oder wählen Sie
     mp4, webm, mkv, avi, mp3, m4a, wav

3. Playlists:
   - Aktivieren Sie die Playlist-Option, um alle Videos einer Playlist herunterzuladen
   - Die Videos werden nummeriert in einem Ordner mit dem Namen der Playlist gespeichert
   - Bei deaktivierter Option lädt eine Playlist-URL nur ein Video herunter

4. Download-Verlauf:
   - Zeigt abgeschlossene und fehlgeschlagene Downloads mit Datum, Qualität und Format
   - Der Verlauf kann gelöscht werden

5. Protokolle:
   - Anwendungsprotokolle anzeigen
   - Protokolle löschen

6. Sprache:
   - Zwischen Englisch, Italienisch, Spanisch, Französisch und Deutsch wechseln

7. Update:
   - Nach Anwendungs-Updates suchen

8. Sponsor:
   - Unterstützen Sie das Projekt mit PayPal oder Monero (QR-Code)
        ''',
        'about_title': 'Über',
        'about_content': '''
Video Downloader v{}

Eine Python-Anwendung zum Herunterladen von Videos aus dem Internet mit yt-dlp.

© Copyright 2024-2026 Tuxxle - Alle Rechte vorbehalten.

Autor: Nsfr750
Website: https://www.tuxxle.org
Email: nsfr750@yandex.com
GitHub: https://github.com/Nsfr750

Organisation: Tuxxle
Lizenz: GPLv3
        ''',
        'sponsor_title': 'Sponsor',
        'sponsor_content': '''
Unterstützen Sie die Entwicklung von Video Downloader

PayPal: https://paypal.me/3dmega

Monero: Siehe QR-Code im Sponsor-Dialog

Vielen Dank für Ihre Unterstützung!
        ''',
        'language_title': 'Sprachauswahl',
        'language_select': 'Sprache auswählen:',
        'language_changed': 'Sprache geändert zu {}',
        'update_title': 'Update',
        'update_checking': 'Suche nach Updates...',
        'update_available': 'Update verfügbar: {}',
        'update_latest': 'Sie verwenden die neueste Version: {}',
        'update_error': 'Fehler beim Suchen nach Updates: {}',
        'log_title': 'Protokoll-Anzeige',
        'log_no_files': 'Keine Protokolldateien gefunden.',
        'back': 'Zurück',
        'close': 'Schließen',
        'yes': 'Ja',
        'no': 'Nein',
        'confirm': 'Bestätigen',
        'cancel': 'Abbrechen',
        'error': 'Fehler',
        'success': 'Erfolg',
        'warning': 'Warnung',
        'info': 'Information',
        'enter_your_choice': 'Geben Sie Ihre Wahl ein:',
        'invalid_choice': 'Ungültige Wahl. Bitte versuchen Sie es erneut.',
        'press_enter_continue': 'Drücken Sie Enter zum Fortfahren...',
        'ui_url_placeholder': 'Video-URL hier eingeben...',
        'ui_add_url': 'URL Hinzufügen',
        'ui_clear_urls': 'URLs Löschen',
        'ui_download': 'Herunterladen',
        'ui_downloading': 'Herunterladen...',
        'ui_progress': 'Fortschritt: {percent:.1f}%',
        'ui_complete': 'Abgeschlossen',
        'ui_failed': 'Fehlgeschlagen',
        'ui_status': 'Status',
        'ui_url_list': 'URL-Liste',
        'ui_download_dir': 'Download-Verzeichnis:',
        'ui_browse': 'Durchsuchen',
        'ui_select_dir': 'Download-Verzeichnis Auswählen',
        'ui_log_viewer': 'Protokoll-Anzeige',
        'ui_refresh_logs': 'Aktualisieren',
        'ui_clear_logs': 'Protokolle Löschen',
        'ui_language': 'Sprache:',
        'ui_sponsor': 'Sponsor',
        'ui_check_updates': 'Nach Updates Suchen',
        'ui_no_urls_added': 'Keine URLs hinzugefügt.',
        'ui_download_started': 'Download gestartet für {count} URL(s)',
        'ui_download_finished': 'Download abgeschlossen',
        'ui_download_summary': 'Download-Zusammenfassung',
        'ui_successful': 'Erfolgreich: {count}',
        'ui_failed_count': 'Fehlgeschlagen: {count}',
        'url_list': 'URL-Liste',
        'menu_history': 'Download-Verlauf',
        'playlist_question': 'Ganze Playlists herunterladen?',
        'yes_no_hint': ' (j/N): ',
        'ui_playlist': 'Ganze Playlist herunterladen (wenn die URL eine Playlist ist)',
        'history_empty': 'Keine Downloads im Verlauf.',
        'history_clear': 'Verlauf Löschen',
        'history_clear_confirm': 'Den gesamten Download-Verlauf löschen?',
        'history_cleared': 'Verlauf gelöscht.',
        'history_col_date': 'Datum',
        'history_col_title': 'Titel',
        'history_col_status': 'Status',
        'history_col_quality': 'Qualität',
        'history_col_format': 'Format',
        'history_col_url': 'URL',
        'history_status_completed': 'Abgeschlossen',
        'history_status_failed': 'Fehlgeschlagen',
    }
}
