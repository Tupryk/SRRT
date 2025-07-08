import time
import h5py
import robotic as ry

class RndConfigs:
    def __init__(self, configfile, datafile):
        self.C = ry.Config()
        self.C.addFile(configfile)
        self.obj = self.C.getFrame('obj')

        file = h5py.File(datafile, 'r')
        self.positions = file['positions'][()]
        print(type(self.positions), self.positions.shape)

    def set_config(self, i):
        self.obj.setPosition(self.positions[i,:3])
        self.C.setJointState(self.positions[i,3:])

    def simulate(self, duration=1.):
        sim = ry.Simulation(self.C, engine=ry.SimulationEngine.physx, verbose=0)

        q = self.C.getJointState()
        tau = .01
        t=0
        while(t<duration):
            sim.step(q, tau, ry.ControlMode.position)
            self.C.view(False, f'simulating t={t:.2f}')
            time.sleep(tau)
            t += tau

    def simulate_all(self):
        for i in range(self.positions.shape[0]):
            self.set_config(i)
            self.simulate(1)
    
    def display_all(self):
        for i in range(self.positions.shape[0]):
            self.set_config(i)
            self.C.view()
            time.sleep(.1)


if __name__ == "__main__":
    D = RndConfigs('twoFingers.yml', 'rnd_twoFingers.h5')
    D.display_all()
    D.simulate_all()
