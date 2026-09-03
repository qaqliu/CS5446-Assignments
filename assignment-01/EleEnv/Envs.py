import numpy as np

class EleEnv:
    def __init__(self, env_config):
        self.env_name = env_config["env_id"]
        self.peo_map = env_config["env_map"]

        self.levels = len(self.peo_map)
        self.act_space = {0: "open door",
                          1: "close door to go",
                          2: "let people in",
                          3: "let people out",
                          4: "go up one level",
                          5: "go down one level"}

        self.all_people = sum(self.peo_map)

        self.cur_level = None  # waiting for reset
        self.peo_ele = None  # 0: empty, 1: people in elevator
        self.ele_door = None  # 0: closed, 1: open

    def reset(self):
        self.cur_level = 0
        self.peo_ele = 0
        self.ele_door = 0

        state = {"elevator_current_level": self.cur_level,
                 "elevator_door": "Open" if self.ele_door == 1 else "Close",
                 "elevator_empty": "Empty" if self.peo_ele == 0 else "Not Empty",
                 "people_at_each_level": self.peo_map}

        return state

    def step(self, action):
        assert self.cur_level is not None, "Please reset the environment first."
        assert action in self.act_space, "Invalid action."

        state = {"elevator_current_level": self.cur_level,
                 "elevator_door": "Open" if self.ele_door == 1 else "Close",
                 "elevator_empty": "Empty" if self.peo_ele == 0 else "Not Empty",
                 "people_at_each_level": self.peo_map}

        reward = 0
        done = False
        info = {}

        if action == 0:
            # action 0: open door
            if self.ele_door == 1:
                return state, reward, done, info
            # open door: let people out if elevator at ground level, otherwise let all people in
            self.ele_door = 1
        elif action == 1:
            # action 1: close door to go
            if self.ele_door == 0:
                return state, reward, done, info
            self.ele_door = 0
        elif action == 2:
            # action 2: let people in
            if self.ele_door == 0 or self.peo_ele == 1:
                # if the door is closed or there are people in the elevator
                return state, reward, done, info

            if self.peo_map[self.cur_level] <= 0:
                # if there are no people at the current level
                return state, reward, done, info
            else:
                # if there are people at the current level
                self.peo_map[self.cur_level] -= 1
                self.peo_ele = 1
        elif action == 3:
            # action 3: let people out
            if self.ele_door == 0 or self.peo_ele == 0:
                # if the door is closed or there are no people in the elevator
                return state, reward, done, info

            self.peo_ele = 0
            self.peo_map[self.cur_level] += 1

            # check if all people are at level 0
            if sum(self.peo_map) == self.all_people and self.peo_map[0] == self.all_people:
                reward = 1
                done = True
        elif action == 4:
            # action 4: go up one level
            if self.ele_door == 1:
                return state, reward, done, info
            if self.cur_level < self.levels - 1:
                self.cur_level += 1
            else:
                return state, reward, done, info
        elif action == 5:
            # action 5: go down one level
            if self.ele_door == 1:
                return state, reward, done, info
            if self.cur_level > 0:
                self.cur_level -= 1
            else:
                return state, reward, done, info

        state = {"elevator_current_level": self.cur_level,
                 "elevator_door": "Open" if self.ele_door == 1 else "Close",
                 "elevator_empty": "Empty" if self.peo_ele == 0 else "Not Empty",
                 "people_at_each_level": self.peo_map}

        return state, reward, done, info

    def render(self):
        for i in range(self.levels - 1, -1, -1):
            if i == self.cur_level:
                if self.ele_door == 0:
                    # the people should be integer
                    print(f"Level {i}\t\tEC[{int(self.peo_ele)}]\t\t{int(self.peo_map[i])}")
                else:
                    print(f"Level {i}\t\tEO[{int(self.peo_ele)}]\t\t{int(self.peo_map[i])}")
            else:
                print(f"Level {i}\t\t~~~~~~\t\t{int(self.peo_map[i])}")

    def action_space(self):
        return self.act_space

    def action_space_sample(self):
        return np.random.choice(list(self.act_space.keys()))
