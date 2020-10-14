
# Function to delete images with cron task
def time_to_delete():
    f_list = os.listdir('cache/')
    if len(f_list) > 50:
        # rm files
        for f in f_list:
            os.remove(f)
            logging.info("Remove %s".format(f))
