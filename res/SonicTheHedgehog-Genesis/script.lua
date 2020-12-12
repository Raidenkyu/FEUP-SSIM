Level_max_x = 0x2560

Prev_lives = 3

function Done()
    local is_done = false
    if data.lives < Prev_lives then is_done = true end
    Prev_lives = data.lives

    if Calc_progress(data) >= 1 then is_done = true end

    -- if Is_stuck(data) then is_done = true end

    -- for debugging
    if is_done then
        print("Frame_count: " .. Frame_count)
        print("Max_x: " .. Max_x)
        print("DONE!")
    end

    return is_done
end

Prev_progress = 0
Frame_count = 0
Frame_limit = 18000

function Reward()
    Frame_count = Frame_count + 1
    local new_progress = Calc_progress(data)
    local reward = (new_progress - Prev_progress) * 9000
    Prev_progress = new_progress

    -- bonus for beating level quickly
    if new_progress >= 1 then
        print("BONUS!")
        reward = reward + (1 - Normalize(Frame_count / Frame_limit, 0, 1)) * 1000
    end
    return reward
end

-- normalizes the value "v" to be between [min, max]
function Normalize(v, min, max)
    if v < min then
        return min
    elseif v > max then
        return max
    else
        return v
    end
end

Offset_x = nil
End_x = nil

-- returns a percentage of completion between [0, 1]
function Calc_progress(data)
    if Offset_x == nil then
        Offset_x = -data.x
        End_x = Level_max_x - data.x
    end

    local cur_x = Normalize(data.x + Offset_x, 0, End_x)
    local ret_value = cur_x / End_x
    return ret_value
end

Max_x = 0
Frames_since_last_max = 0

-- returns true if the agent has not progressed in a while
function Is_stuck(data)

    local new_max = math.max(Max_x, data.x + Offset_x)

    if new_max > Max_x then
        Frames_since_last_max = 0
    else
        Frames_since_last_max = Frames_since_last_max + 1
    end
    Max_x = new_max

    local is_stuck = false
    if Frames_since_last_max > 1000 then is_stuck = true end

    return is_stuck
end

