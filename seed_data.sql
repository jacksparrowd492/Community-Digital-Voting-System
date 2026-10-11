-- Seed Data for Community Digital Voting System
-- Resets the database to exactly five fresh proposals:
-- 3 active, 1 closed, 1 expired. No votes.

-- Remove all existing data (votes first because of the foreign key)
DELETE FROM votes;
DELETE FROM proposals;

-- 1. Active Proposal (Deadline in 7 days)
INSERT INTO proposals (title, description, created_at, deadline, status)
VALUES (
    'Build a Community Vegetable Garden',
    'Convert the unused lot behind the library into a shared vegetable garden with raised beds and a water connection for residents.',
    datetime('now'),
    datetime('now', '+7 days'),
    'active'
);

-- 2. Active Proposal (Deadline in 5 days)
INSERT INTO proposals (title, description, created_at, deadline, status)
VALUES (
    'Install LED Street Lights on Park Avenue',
    'Replace the old sodium street lights on Park Avenue with energy-efficient LED fixtures to improve night-time safety and cut electricity costs.',
    datetime('now'),
    datetime('now', '+5 days'),
    'active'
);

-- 3. Active Proposal (Deadline in 3 days)
INSERT INTO proposals (title, description, created_at, deadline, status)
VALUES (
    'Weekend Free Coding Classes for Youth',
    'Run free Saturday coding workshops for residents aged 12-18 at the community center, taught by volunteer software engineers.',
    datetime('now'),
    datetime('now', '+3 days'),
    'active'
);

-- 4. Closed Proposal (Closed by Admin before its deadline)
INSERT INTO proposals (title, description, created_at, deadline, status)
VALUES (
    'Add Recycling Bins Near the Bus Stops',
    'Place separate paper, plastic and glass recycling bins at every bus stop in the neighborhood.',
    datetime('now', '-6 days'),
    datetime('now', '+4 days'),
    'closed'
);

-- 5. Expired Proposal (Deadline passed 2 days ago)
INSERT INTO proposals (title, description, created_at, deadline, status)
VALUES (
    'Monthly Neighborhood Clean-Up Drive',
    'Organize a volunteer clean-up drive on the first Sunday of every month, with gloves and bags supplied by the community fund.',
    datetime('now', '-10 days'),
    datetime('now', '-2 days'),
    'expired'
);
