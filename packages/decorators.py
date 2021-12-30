'''

    裝飾器的東西

'''

def execut_time(func):
    ''' 計算程式執行時間 '''

    def decorator(*args, **kwargs):
        import time
        start = time.time()
        func(*args, **kwargs)

        print(f'Execut Time : {time.time() - start} s.')
    
    return decorator

