
-- 创建触发器：检查战队是否存在
DELIMITER //
CREATE TRIGGER before_player_insert
BEFORE INSERT ON players
FOR EACH ROW
BEGIN
    DECLARE team_count INT;
    SELECT COUNT(*) INTO team_count FROM teams WHERE team_name = NEW.team_name;
    IF team_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '战队不存在，请先创建战队';
    END IF;
END;
//
DELIMITER ;

-- 创建触发器：确保选手号码唯一
DELIMITER //
CREATE TRIGGER unique_player_number
BEFORE INSERT ON players
FOR EACH ROW
BEGIN
    DECLARE player_count INT;
    SELECT COUNT(*) INTO player_count FROM players WHERE team_name = NEW.team_name AND player_number = NEW.player_number;
    IF player_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '该战队的选手号码已存在';
    END IF;
END;
//
DELIMITER ;

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_win_rate`(IN team VARCHAR(255), IN new_rate FLOAT)
BEGIN
    DECLARE teamExists INT DEFAULT 0;

    IF new_rate >= 0 AND new_rate <= 1 THEN
        SELECT COUNT(*) INTO teamExists FROM participations WHERE team_name = team;

        IF teamExists > 0 THEN
            UPDATE teams SET recent_win_rate = new_rate WHERE team_name = team;
        ELSE
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '该战队未参加任何比赛';
        END IF;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '胜率必须在0到1之间';
    END IF;
END

-- 创建视图：team_players
CREATE VIEW team_players AS
SELECT teams.team_name, players.player_number, players.name,
players.birthdate, players.nationality, players.position
FROM teams
JOIN players ON teams.team_name = players.team_name;
