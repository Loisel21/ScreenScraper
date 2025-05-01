from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast("Titel der Nachricht", "Dies ist der Nachrichtentext", duration=5)