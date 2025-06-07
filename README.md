# Knapsack Problem - Harmony Search
Решение задачи о рюкзаке при помощи алгоритма поиска гармонии.

## Интерфейс / Interface

- **Кнопка "Load Items"**: Загружает список элементов (вес и ценность) из текстового файла / Loads a list of items (weight and value) from a text file.
- **Кнопка "Load Parameters"**: Загружает параметры алгоритма из текстового файла / Loads algorithm parameters from a text file.
- **Кнопка "Run Algorithm"**: Запускает алгоритм поиска гармонии / Runs the Harmony Search algorithm.
- **Кнопка "Switch to Light Theme" / "Switch to Dark Theme"**: Переключает тему интерфейса между светлой ("litera") и темной ("darkly") / Toggles the interface theme between light ("litera") and dark ("darkly").
- **Кнопка "Show Convergence Plot"**: Отображает график сходимости / Displays a convergence plot.
- **Текстовое поле**: Показывает информацию о загруженных данных и результаты / Displays information about loaded data and results.

## Формат входных файлов / Input File Formats

### 1. Файл элементов (items.txt) / Items File (items.txt)
- Каждая строка содержит два числа, разделенных пробелом: `<вес> <ценность>` / Each line contains two numbers separated by a space: `<weight> <value>`.
- Вес и ценность — числа (целые или с плавающей точкой) / Weight and value must be numbers (integers or floating-point).

### 2. Файл параметров (parameters.txt) / Parameters File (parameters.txt)
Содержит 7 строк с параметрами / Contains 7 lines with parameters:
- Максимальный вес рюкзака (положительное число) / Maximum knapsack weight (positive number).
- Размер гармонической памяти (hms, целое положительное число) / Harmony memory size (hms, positive integer).
- Коэффициент выбора гармонии (hmcr, число от 0 до 1) / Harmony memory consideration rate (hmcr, number between 0 and 1).
- Коэффициент корректировки (par, число от 0 до 1) / Pitch adjustment rate (par, number between 0 and 1).
- Максимальное количество итераций (max_iter, целое положительное число) / Maximum number of iterations (max_iter, positive integer).
- Имя изменяемого параметра (одно из: hms, hmcr, par, max_iter) / Name of the parameter to vary (one of: hms, hmcr, par, max_iter).
- Список значений для изменяемого параметра (через пробел) / List of values for the varied parameter (space-separated).

## Использование / Usage

1. **Запуск программы / Launching the Program**:
   - Запустите `.exe` файл. Откроется окно с темной темой / Run the `.exe` file. The window opens with the dark theme.

2. **Загрузка элементов / Loading Items**:
   - Нажмите "Load Items" и выберите файл (например, `items.txt`) / Click "Load Items" and select a file (e.g., `items.txt`).
   - Информация о загруженных элементах появится в текстовом поле / Loaded items will appear in the text area.

3. **Загрузка параметров / Loading Parameters**:
   - Нажмите "Load Parameters" и выберите файл (например, `parameters.txt`) / Click "Load Parameters" and select a file (e.g., `parameters.txt`).
   - Информация о параметрах отобразится в текстовом поле / Loaded parameters will appear in the text area.
   - При некорректных параметрах появится сообщение об ошибке / Invalid parameters will trigger an error message.

4. **Запуск алгоритма / Running the Algorithm**:
   - Убедитесь, что элементы и параметры загружены / Ensure items and parameters are loaded.
   - Нажмите "Run Algorithm" / Click "Run Algorithm".
   - Алгоритм выполнится для каждого значения изменяемого параметра / The algorithm runs for each value of the varied parameter.
   - Результаты (решение, ценность, вес, время выполнения, итерация) отобразятся в текстовом поле / Results (solution, value, weight, execution time, iteration) will appear in the text area.

5. **Смена темы / Switching Themes**:
   - Нажмите "Switch to Light Theme" для светлой темы / Click "Switch to Light Theme" for the light theme.
   - Кнопка изменится на "Switch to Dark Theme" / The button changes to "Switch to Dark Theme".
   - Повторное нажатие вернет темную тему / Clicking again reverts to the dark theme.
   - Тема влияет на интерфейс и графики / The theme affects the interface and plot styles.

6. **График сходимости / Convergence Plot**:
   - После выполнения алгоритма нажмите "Show Convergence Plot" / After running the algorithm, click "Show Convergence Plot".
   - Откроется график сходимости для каждого значения параметра / A plot shows the objective function over iterations for each parameter value.
   - График адаптируется к текущей теме / The plot adapts to the current theme.

## Возможные ошибки / Possible Errors

- **"Please load items and parameters first!"**: Попытка запустить алгоритм без данных / Attempt to run the algorithm without loading data.
- **"No feasible solution exists: all items exceed max_weight!"**: Все элементы превышают максимальный вес / All items exceed the maximum weight.
- **"Failed to load items/parameters"**: Неверный формат файла или ошибка чтения / Invalid file format or reading error.
- **"Run the algorithm first!"**: Попытка построить график без запуска алгоритма / Attempt to display the plot without running the algorithm.
