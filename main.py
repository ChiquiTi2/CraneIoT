from crane_simulation.sensors import Crane
import continuous_threading


if __name__ == '__main__':
    My_Crane = Crane(1)
    # My_Crane.run_crane()
    print(My_Crane.rot_sensor().render())
    try:
        #sensor_thread = continuous_threading.Thread(target=temp_sensor, name="Sensor_Thread")
        #sensor_thread.start()
        pass
    except:
        print("Unable to start thread")
