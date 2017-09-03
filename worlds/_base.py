
import mandalka

def build_table_world(self, build_table):
    import os
    import numpy as np

    path = ("__cache__/" + self.__class__.__name__.lower()
        + "_" + mandalka.unique_id(self))

    if os.path.exists(path):
        inputs = np.load(path + "/inputs.npy", mmap_mode="r")
        labels = np.load(path + "/labels.npy", mmap_mode="r")
    else:
        os.makedirs(path + ".tmp", exist_ok=True)
        inputs, labels = build_table()
        assert len(inputs) == len(labels)
        np.save(path + ".tmp/inputs.npy", inputs)
        np.save(path + ".tmp/labels.npy", labels)
        os.rename(path + ".tmp", path)

    self.get_observation_shape = lambda: inputs[0].shape
    self.get_action_shape = lambda: labels[0].shape
    self.get_reward_shape = lambda: labels[0].shape

    def trajectory_batch(agent, seed_batch):
        # Assume seeds passed from the top are sensible
        idx = [seed % len(inputs) for seed in seed_batch]

        # Request predictions from the outer agent
        _, pred_batch = agent.step([None] * len(idx), inputs[idx])
        pred_batch = np.asarray(pred_batch)
        assert pred_batch.shape == (len(idx),) + labels[0].shape

        # Gradient (label - prediction) is correct for
        # 1/2 MSE and also for softmax + cross entropy (!)
        return [
            [(inputs[i], pred, labels[i] - pred)]
            for i, pred in zip(idx, pred_batch)
        ]

    self.trajectory_batch = trajectory_batch