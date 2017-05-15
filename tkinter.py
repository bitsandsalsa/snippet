import threading
import Tkinter as tk
import tkMessageBox
import ttk

# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
# http://www.tkdocs.com/index.html

# show available themes
sty = ttk.Style()
sty.theme_names()

# show theme in use
sty.theme_use()

# change theme (can change at runtime after widgets are created)
sty.theme_use('classic')


class LifetimeError(Exception):
    pass

# Example Tkinter app. A progress bar.
class GuiProgressBar(ttk.Frame):
    def __init__(self, title, work_count, work_func, *func_args):
        ttk.Frame.__init__(self, relief='ridge', borderwidth=2)
        self.work_count = work_count
        self.worker_task = threading.Thread(target=work_func, args=func_args)
        self.is_pending_quit = False
        self.master.title(title)
        self.pack(fill='both', expand=1)  # fill both x and y directions, expand with window changes
        self._create_widgets()

    def _create_widgets(self):
        self.my_button_text = tk.StringVar(value='Start')
        self.my_button = ttk.Button(self, textvariable=self.my_button_text, command=self._start)
        self.my_button.pack()

        self.my_label_frame = ttk.LabelFrame(self, text='Work Items')
        self.my_label_frame.pack(fill='x')

        self.my_label_text = tk.StringVar()
        self.my_label = ttk.Label(self.my_label_frame, anchor='w', textvariable=self.my_label_text)
        self.my_label.pack(fill='x')

        self.my_progress_bar = ttk.Progressbar(
            self,
            orient='horizontal',
            length=self.master.winfo_screenwidth()/5,
            mode='determinate',
            maximum=self.work_count
        )
        self.my_progress_bar.pack(fill='both')

        self.my_status_label_text = tk.Stringvar(value='0 / {}'.format(self.work_count))
        self.my_status_label = ttk.Label(self, anchor='w', textvariable=self.my_status_label_text)
        self.my_status_label.pack(fill='x')

    def _confirm_quit(self):
        if tkMessageBox.askyesno(message='Quit?'):
            self.is_pending_quit = True
            self.master.destroy()

    def _start(self):
        self.my_button.state(['disabled'])
        self.my_button_text.set('Running...')
        # Schedule a new thread. Can't use "after" function because a long running task would stall
        # the GUI mainloop and GUI would become unresponsive. The "after" function seems to add
        # tasks to an ordered work queue where one task runs at a time.
        self.worker_task.start()

    def update_progress(self, delta):
        if self.is_pending_quit:
            raise LifetimeError('User initiated quit.')
        self.my_progress_bar.step(delta)
        self.my_status_label_text.set('{} / {}'.format(
            int(self.my_progress_bar['value']) + delta,
            self.work_count
        ))

    def update_work_item_text(self, work_itme):
        self.my_label_text.set(work_item)

    def finish_work(self):
        self.my_button.state(['disabled'])
        self.my_button_text.set('Finished')

class Worker(object):
    def __init__(self):
        self.progress_bar = None
        self.work_items = get_work_items()

    def start(self):
        self.progress_bar = GuiProgressBar('The Worker', len(self.work_items), self.do_work)
        self.progress_bar.mainloop()

    def do_work(self):
        try:
            for item in self.work_items:
                self.progress_bar.update_work_item_text(str(item))

                # calculations

                self.progress_bar.update_progress(1)
            self.progress_bar.finish_work()
        except LifetimeError as e:
            print e
