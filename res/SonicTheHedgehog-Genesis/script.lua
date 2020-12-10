level_max_x = 0x2560

prev_lives = 3

function done()
    if data.lives < prev_lives then return true end
    prev_lives = data.lives

    if calc_progress(data) >= 1 then return true end

    return false
end

prev_progress = 0
frame_count = 0
frame_limit = 18000

function reward()
    frame_count = frame_count + 1
    local progress = calc_progress(data)
    local reward = (progress - prev_progress) * 9000
    prev_progress = progress

    -- bonus for beating level quickly
    if progress >= 1 then
        reward = reward + (1 - clip(frame_count / frame_limit, 0, 1)) * 1000
    end
    return reward
end

function clip(v, min, max)
    if v < min then
        return min
    elseif v > max then
        return max
    else
        return v
    end
end

offset_x = nil
end_x = nil

function calc_progress(data)
    if offset_x == nil then
        offset_x = -data.x
        local key = string.format("zone=%d,act=%d", data.zone, data.act)
        end_x = level_max_x - data.x
    end

    local cur_x = clip(data.x + offset_x, 0, end_x)
    return cur_x / end_x
end


