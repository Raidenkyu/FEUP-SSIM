Level_max_x = 0x2560

Prev_lives = 3

--[[
 - The reward function needs adjustments
    - Max(x) may need rework
    - When dying, the negative reward may need adjustment
    - When winning, the bonus may need adjustment
    - 10x multiplier may need adjustment
]]

function Done()
    -- TODO: change is_done to an enum (dead, stuck, alive, etc), to use in reward function
    local is_done = false
    if data.lives < Prev_lives then is_done = true end

    if Calc_progress(data) >= 1 then is_done = true end

    if Frame_count > 35000 then is_done = true end -- TODO: might need to be removed

    -- TODO: maybe add a case for when stuck, not yet sure if that helps

    -- for debugging
    if is_done then
        Print_state("DONE!")
    end

    return is_done
end

Prev_progress = 0
Frame_count = 0
Frame_limit = 18000 -- 36102 is the 10min timeout
Total_reward = 0
Max_x = 0
Ring_count = nil

function Reward()

    -- TODO: consider scenario in which the agent died by getting stuck
    if data.lives < Prev_lives then
        Print_tab("DEAD")
        return -1
    end

    Update_max()
    local new_reward = Get_reward()
    Total_reward = Total_reward + new_reward

    return new_reward

end

function Get_reward()

    -- if Ring_count == nil then
    --     -- first time
    --     if data.rings > 0 then
    --         Ring_count = data.rings
    --         Print_tab("FIRST RINGS: " .. Ring_count)
    --     end
    -- elseif Ring_count ~= data.rings then
    --     if data.rings < Ring_count then
    --         Ring_count = data.rings
    --         Print_tab("LOST RINGS: " .. Ring_count)
    --         return -0.5
    --     end

    --     Ring_count = data.rings
    --     Print_tab("NEW RINGS: " .. Ring_count)
    -- end

    Frame_count = Frame_count + 1
    local new_progress = Calc_progress(data)
    local reward = (new_progress - Prev_progress) * 10

    Prev_progress = new_progress

    -- bonus for beating level quickly
    -- if Calc_progress(data) >= 1 then
    --     local bonus = (1 - Normalize(Frame_count / Frame_limit, 0, 1)) * 10
    --     print("BONUS: " .. bonus)
    --     reward = reward + bonus
    -- end
    return reward
end

function Update_max()
    local new_max = math.max(Max_x, data.x + Offset_x)

    -- FOR DEBUG
    if new_max > Max_x then
        -- Print_tab("new_max: " .. new_max)
    end

    Max_x = new_max
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

-- returns a percentage of completion between [0, 1] (using Max_x) (DEPRECATED)
function Calc_progress_max()
    local cur_x = Normalize(Max_x, 0, End_x)
    local ret_value = cur_x / End_x
    return ret_value
end

-- Print functions, for debugging
function Print_state(msg)
    Print_tab("=================================")
    Print_tab(msg)
    Print_tab("Frame_count: " .. Frame_count)
    Print_tab("Progress: " .. (Calc_progress(data) * 100) .. "%" )
    Print_tab("Total_reward: " .. Total_reward)
    Print_tab("Lives: " .. data.lives)
    Print_tab("=================================")
end

function Print_tab(msg)
    print("\t\t\t\t\t\t\t\t" .. msg)
end