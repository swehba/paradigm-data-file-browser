from action_data_file_manager import ActionDataFileManager, SortBy, SortOrder


# noinspection PyMethodMayBeStatic
class Application:

    def __init__(self):
        self.file_manager = ActionDataFileManager()

    def print_header(self, header):
        print()
        print(header)
        print('-' * len(header))

    def input_int(self, prompt):
        try:
            i = int(input(prompt))
            return i if i > 0 else None
        except TypeError:
            return None

    def input_list(self, prompt):
        try:
            s = input(prompt)
            result = [item.strip() for item in s.split(',')]
            return result if len(result) > 0 else None
        except:
            return None

    def filter_menu(self):
        while True:
            self.print_header('Filter Menu')
            print(f' 1 - min file size ({self.file_manager.min_file_size})')
            print(f' 2 - max file size ({self.file_manager.max_file_size})')
            print(f' 3 - sensor locations ({self.file_manager.sensor_locations})')
            print(f' 4 - min samples ({self.file_manager.min_samples})')
            print(f' 5 - max samples ({self.file_manager.max_samples})')
            print(f' 6 - action types ({self.file_manager.action_types})')
            print(f'99 - DONE')
            print()
            selection = str(input('Selection: '))

            if selection == '1':
                self.file_manager.min_file_size = self.input_int('Enter min file size: ')
            elif selection == '2':
                self.file_manager.max_file_size = self.input_int('Enter max file size: ')
            elif selection == '3':
                self.file_manager.sensor_locations = self.input_list('Enter sensor locations separated by commas: ')
            elif selection == '4':
                self.file_manager.min_samples = self.input_int('Enter min number of samples: ')
            elif selection == '5':
                self.file_manager.max_samples = self.input_int('Enter max number of samples: ')
            elif selection == '6':
                self.file_manager.action_types = self.input_list('Enter action types separated by commas: ')
            elif selection == '99':
                return

    def clear_filters(self):
        self.file_manager.clear_filters()

    def sort_menu(self):
        self.print_header('Sort Menu')
        print('1 - file name, ascending')
        print('2 - file name, descending')
        print('3 - file size, ascending')
        print('4 - file size, descending')
        print('5 - sample count, ascending')
        print('6 - sample count, descending')
        print('')
        choice = str(input('Selection: '))

        if choice == '1':
            self.file_manager.sort_by = SortBy.file_name
            self.file_manager.sort_order = SortOrder.ascending
        elif choice == '2':
            self.file_manager.sort_by = SortBy.file_name
            self.file_manager.sort_order = SortOrder.descending
        elif choice == '3':
            self.file_manager.sort_by = SortBy.file_size
            self.file_manager.sort_order = SortOrder.ascending
        elif choice == '4':
            self.file_manager.sort_by = SortBy.file_size
            self.file_manager.sort_order = SortOrder.descending
        elif choice == '5':
            self.file_manager.sort_by = SortBy.file_size
            self.file_manager.sort_order = SortOrder.ascending
        elif choice == '6':
            self.file_manager.sort_by = SortBy.file_size
            self.file_manager.sort_order = SortOrder.descending

    def change_folder(self):
        print()
        print(f'Current data files folder is "{self.file_manager.folder}".')
        folder = input('Enter path to data files folder: ')
        if folder:
            self.file_manager.load_folder(folder)

    def main_menu(self):
        self.print_header('Main Menu')
        print(' 1 - Filter files')
        print(' 2 - Clear all filters')
        print(' 3 - Sort files')
        print(' 4 - Change data files folder')
        print('99 - Quit')
        print()
        selection = str(input('Selection: '))
        if selection == '1':
            self.filter_menu()
        elif selection == '2':
            self.clear_filters()
        elif selection == '3':
            self.sort_menu()
        elif selection == '4':
            self.change_folder()
        elif selection == '99':
            exit(0)

    def run(self):
        self.change_folder()

        while True:
            print()
            dashes = '-' * 100
            print('{:33}  {:>10}  {:10}  {:10}  {:>10}  {:10}  {:>4}  {:8}'.format('File', 'Size', 'Action', 'Location',
                                                                                   'Samples', 'Watch', 'Freq',
                                                                                   'Distance'))
            print('{0:.33}  {0:.10}  {0:.10}  {0:.10}  {0:.10}  {0:.10}  {0:>.4}  {0:.8}'.format(dashes))

            for file in self.file_manager:
                print(f'{file.name_noext:33}  {file.size:>10,}  {file.action_type:10}  {file.sensor_location:10}  '
                      f'{file.gyro_sample_count:10,}  {file.watch_model:10}  {file.sampling_frequency:>4}  '
                      f'{file.distance:8}')

            self.main_menu()


if __name__ == '__main__':
    app = Application()
    app.run()
