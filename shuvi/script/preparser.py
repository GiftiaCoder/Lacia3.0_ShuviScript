class Parser:
    def __init__(self):
        # statement machine stat from stat_1
        self.__cur_stat__ = self.__stat_1__
        # keep cur text
        self.__cur_txt__ = ''
        # whether we should close the parser when deconstructing
        self.__alive__ = True
        # context
        self.__exec_context__ = {
            'print': self.__print__
        }
        # full script
        self.final_script = ''

    def feed(self, c):
        """
        move statement
        """
        self.__cur_stat__ = self.__cur_stat__(c)

    def get_final_script(self):
        return self.final_script

    def close(self):
        """
        close the parser
        """
        if self.__cur_stat__ != self.__stat_1__:
            raise Exception('invalid statement when exit, please check your script syntax')
        if self.__alive__ and len(self.__cur_txt__) > 0:
            self.__print_txt__()

            self.__cur_stat__ = self.__stat_1__
            self.__cur_txt__ = ''
            self.__exec_context__ = {
                'print': self.__print__
            }
            self.__alive__ = False

    def __print_txt__(self):
        """
        print script text directly
        """
        self.final_script += self.__cur_txt__
        self.__cur_txt__ = ''

    def __exec_script__(self):
        """
        exec python script
        """
        exec(self.__cur_txt__, self.__exec_context__)
        self.__cur_txt__ = ''

    def __print__(self, *vals):
        for val in vals:
            self.final_script += ('%s' % val).strip()
            self.final_script += '\n'

    # statement machine from here
    def __stat_1__(self, c):
        if c == '{':
            return self.__stat_2__
        else:
            self.__cur_txt__ += c
            return self.__stat_1__

    def __stat_2__(self, c):
        if c == '{':
            self.__print_txt__()
            return self.__stat_3__
        else:
            self.__cur_txt__ += '{'
            self.__cur_txt__ += c
            return self.__stat_1__

    def __stat_3__(self, c):
        if c == '}':
            return self.__stat_4__
        else:
            self.__cur_txt__ += c
            return self.__stat_3__

    def __stat_4__(self, c):
        if c == '}':
            self.__exec_script__()
            return self.__stat_1__
        else:
            self.__cur_txt__ += '}'
            self.__cur_txt__ += c
            return self.__stat_3__

    def __del__(self):
        self.close()

