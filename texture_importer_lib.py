import os
import shutil
from datetime import datetime


class TextureImporterLib(object):
    """Library for Texture Importer tool."""

    @staticmethod
    def processing_folder_nomenclature(name, types, log_msg):
        """Validate the nomenclature of a folder. Return the result and log info."""

        if name in types:  # Source B - folder
            log_msg += '{} :: {}\n'.format(str(datetime.now()), '{} folder with valid nomenclature.'.format(name))
            return name, log_msg

        log_msg += '{} :: {}\n'.format(str(datetime.now()), '{} folder with invalid nomenclature. Ignored.'.format(name))
        return False, log_msg

    @staticmethod
    def processing_file_nomenclature(name, types, extensions, log_msg):
        """Validate the nomenclature of a file and collect data. Return the result and log info."""

        type_ = ''
        variation = ''
        description = ''
        udim = ''
        extension = ''

        name_splitted = name.split('.')

        if len(name_splitted) == 3:

            filename = name_splitted[0]
            udim = name_splitted[1]
            extension = name_splitted[2]

            if extension in extensions and len(udim) == 4:

                filename_splitted = filename.split('_')

                if len(filename_splitted) == 1:
                    description = filename_splitted[0]

                if len(filename_splitted) == 2:

                    description = filename_splitted[0]
                    type_ = filename_splitted[1]

                    if not type_ in types:
                        log_msg += '{} :: {}\n'.format(str(datetime.now()), '{} type invalid in nomenclature. Ignored.'.format(type_))
                        type_ = ''

                if len(filename_splitted) == 3:

                    description = filename_splitted[0]
                    variation = filename_splitted[1]
                    type_ = filename_splitted[2]

                    if not type_ in types:
                        log_msg += '{} :: {}\n'.format(str(datetime.now()), '{} type invalid in nomenclature. Ignored.'.format(type_))
                        type_ = ''

            else:
                log_msg += '{} :: {}\n'.format(str(datetime.now()), '{} file ignored by invalid extension and/or UDIM padding.'.format(name))
        else:
            log_msg += '{} :: {}\n'.format(str(datetime.now()), '{} file ignored by invalid nomenclature.'.format(name))

        return type_, variation, description, udim, extension, log_msg

    @staticmethod
    def processing_copy(source_directory, filename, destination_directory, type_, variation,
                        description, udim, extension, log_msg):
        """Prepare the output path per file and execute the copy. Return the result and log info."""

        source_path = '{}/{}'.format(source_directory, filename)

        if not variation:
            variation = 'main'

        variation_directory = '{}/{}'.format(destination_directory, variation)

        if not os.path.exists(variation_directory):
            os.mkdir(variation_directory)

        description_directory = '{}/{}'.format(variation_directory, description)

        if not os.path.exists(description_directory):
            os.mkdir(description_directory)

        destination_filename = '{}.{}.{}'.format(type_, udim, extension)

        destination_path = '{}/{}'.format(description_directory, destination_filename)

        result = shutil.copyfile(src=source_path, dst=destination_path)

        log_msg += '{} :: {}\n'.format(str(datetime.now()), '{} file copied successfully.'.format(filename))

        return result, log_msg

    @staticmethod
    def analyzing_input_data(source_directory, destination_directory, extensions, types, log_msg):
        """Start the analysis process of input. Return the result and log info."""

        result = []
        files_counter = 0

        for dirpath, dirnames, filenames in os.walk(source_directory):

            if dirpath == source_directory and filenames:  # Source A

                files_counter += len(filenames)

                for filename in filenames:

                    log_msg += '{} :: {}\n'.format(str(datetime.now()), 'Processing nomenclature of {}'.format(filename))

                    type_, variation, description, udim, extension, log_msg = TextureImporterLib.processing_file_nomenclature(name=filename,
                                                                                                                              types=types,
                                                                                                                              extensions=extensions,
                                                                                                                              log_msg=log_msg)

                    if type_:

                        result_copy, log_msg = TextureImporterLib.processing_copy(source_directory=source_directory,
                                                                                  filename=filename,
                                                                                  destination_directory=destination_directory,
                                                                                  type_=type_, variation=variation,
                                                                                  description=description,
                                                                                  udim=udim, extension=extension,
                                                                                  log_msg=log_msg)

                        result.append(result_copy)

            if dirpath == source_directory and dirnames:  # Source B
                for dirname in dirnames:
                    type_, log_msg = TextureImporterLib.processing_folder_nomenclature(name=dirname,
                                                                              types=types,
                                                                              log_msg=log_msg)

                    if type_:

                        source_b_directory = '{}/{}'.format(source_directory, type_)

                        for dirpath, dirnames, filenames in os.walk(source_b_directory):
                            if dirpath == source_b_directory and filenames:

                                files_counter += len(filenames)

                                for filename in filenames:
                                    _, variation, description, udim, extension, log_msg = TextureImporterLib.processing_file_nomenclature(name=filename,
                                                                                                                                          types=types,
                                                                                                                                          extensions=extensions,
                                                                                                                                          log_msg=log_msg)

                                    result_copy, log_msg = TextureImporterLib.processing_copy(source_directory=source_b_directory,
                                                                                              filename=filename,
                                                                                              destination_directory=destination_directory,
                                                                                              type_=type_, variation=variation,
                                                                                              description=description,
                                                                                              udim=udim, extension=extension,
                                                                                              log_msg=log_msg)

                                    result.append(result_copy)

        log_msg += '{} :: {}\n'.format(str(datetime.now()), 'Import process finalized.')

        return result, files_counter, log_msg
