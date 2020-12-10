Level_max_x = 0x2560

Prev_lives = 3

function Done()
    local is_done = false
    if data.lives < Prev_lives then is_done = true end
    Prev_lives = data.lives

    if Calc_progress(data) >= 1 then is_done = true end

    if is_done then print("DONE!") end

    return is_done
end

Prev_progress = 0
Frame_count = 0
Frame_limit = 18000

function Reward()
    Frame_count = Frame_count + 1
    local progress = Calc_progress(data)
    local reward = (progress - Prev_progress) * 9000
    Prev_progress = progress

    -- bonus for beating level quickly
    if progress >= 1 then
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


