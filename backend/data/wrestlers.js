const wrestlers = [
  {
    id: 'john-cena',
    name: 'John Cena',
    nickname: 'The Cenation Leader',
    realName: 'John Felix Anthony Cena Jr.',
    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&crop=face',
    age: 46,
    height: '6\'1"',
    weight: '251 lbs',
    hometown: 'West Newbury, Massachusetts',
    signatureMoves: ['Attitude Adjustment', 'Five Knuckle Shuffle', 'STF/STFU'],
    recentMatches: [
      { id: '1', opponent: 'Roman Reigns', result: 'L', date: '2024-01-15', event: 'WrestleMania 40' },
      { id: '2', opponent: 'Seth Rollins', result: 'W', date: '2024-01-08', event: 'Monday Night Raw' },
      { id: '3', opponent: 'Drew McIntyre', result: 'W', date: '2024-01-01', event: 'New Year\'s Revolution' },
      { id: '4', opponent: 'Kevin Owens', result: 'L', date: '2023-12-25', event: 'Holiday Havoc' },
      { id: '5', opponent: 'CM Punk', result: 'W', date: '2023-12-18', event: 'Monday Night Raw' },
    ],
    momentumScore: 11,
    careerStats: {
      totalMatches: 2847,
      wins: 1892,
      losses: 832,
      draws: 123,
      winPercentage: 66.4,
    },
    championships: [
      '16x WWE Champion',
      '5x United States Champion',
      '4x Tag Team Champion',
      '2x Royal Rumble Winner'
    ],
    bio: 'One of the most recognizable faces in sports entertainment, John Cena has been a cornerstone of WWE for over two decades.'
  },
  {
    id: 'roman-reigns',
    name: 'Roman Reigns',
    nickname: 'The Tribal Chief',
    realName: 'Leati Joseph Anoa\'i',
    image: 'https://images.unsplash.com/photo-1566492031773-4f4e44671d66?w=400&h=400&fit=crop&crop=face',
    age: 38,
    height: '6\'3"',
    weight: '265 lbs',
    hometown: 'Pensacola, Florida',
    signatureMoves: ['Spear', 'Superman Punch', 'Guillotine Choke'],
    recentMatches: [
      { id: '1', opponent: 'Cody Rhodes', result: 'L', date: '2024-01-20', event: 'WrestleMania 40' },
      { id: '2', opponent: 'John Cena', result: 'W', date: '2024-01-15', event: 'WrestleMania 40' },
      { id: '3', opponent: 'LA Knight', result: 'W', date: '2024-01-10', event: 'SmackDown' },
      { id: '4', opponent: 'Kevin Owens', result: 'W', date: '2024-01-03', event: 'SmackDown' },
      { id: '5', opponent: 'Solo Sikoa', result: 'W', date: '2023-12-27', event: 'SmackDown' },
    ],
    momentumScore: 13,
    careerStats: {
      totalMatches: 1456,
      wins: 987,
      losses: 398,
      draws: 71,
      winPercentage: 67.8,
    },
    championships: [
      '4x WWE Champion',
      '3x Universal Champion',
      '1x Intercontinental Champion',
      '1x Tag Team Champion',
      '1x Royal Rumble Winner'
    ],
    bio: 'The head of the table and leader of The Bloodline, Roman Reigns has dominated WWE as the Tribal Chief.'
  },
  {
    id: 'cody-rhodes',
    name: 'Cody Rhodes',
    nickname: 'The American Nightmare',
    realName: 'Cody Garrett Runnels',
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face',
    age: 38,
    height: '6\'1"',
    weight: '219 lbs',
    hometown: 'Marietta, Georgia',
    signatureMoves: ['Cross Rhodes', 'Cody Cutter', 'Figure Four Leglock'],
    recentMatches: [
      { id: '1', opponent: 'Roman Reigns', result: 'W', date: '2024-01-20', event: 'WrestleMania 40' },
      { id: '2', opponent: 'Seth Rollins', result: 'W', date: '2024-01-12', event: 'Royal Rumble' },
      { id: '3', opponent: 'Drew McIntyre', result: 'W', date: '2024-01-05', event: 'Monday Night Raw' },
      { id: '4', opponent: 'Gunther', result: 'L', date: '2023-12-28', event: 'Monday Night Raw' },
      { id: '5', opponent: 'Damian Priest', result: 'W', date: '2023-12-21', event: 'Monday Night Raw' },
    ],
    momentumScore: 14,
    careerStats: {
      totalMatches: 1823,
      wins: 1245,
      losses: 456,
      draws: 122,
      winPercentage: 68.3,
    },
    championships: [
      '1x WWE Champion',
      '2x Intercontinental Champion',
      '6x Tag Team Champion',
      '1x TNT Champion (AEW)'
    ],
    bio: 'The American Nightmare returned to WWE to finish his story and capture the WWE Championship at WrestleMania 40.'
  },
  {
    id: 'seth-rollins',
    name: 'Seth Rollins',
    nickname: 'The Visionary',
    realName: 'Colby Daniel Lopez',
    image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face',
    age: 37,
    height: '6\'1"',
    weight: '217 lbs',
    hometown: 'Davenport, Iowa',
    signatureMoves: ['Stomp', 'Pedigree', 'Superkick'],
    recentMatches: [
      { id: '1', opponent: 'Cody Rhodes', result: 'L', date: '2024-01-12', event: 'Royal Rumble' },
      { id: '2', opponent: 'John Cena', result: 'L', date: '2024-01-08', event: 'Monday Night Raw' },
      { id: '3', opponent: 'CM Punk', result: 'W', date: '2024-01-01', event: 'Monday Night Raw' },
      { id: '4', opponent: 'Damian Priest', result: 'W', date: '2023-12-25', event: 'Monday Night Raw' },
      { id: '5', opponent: 'Gunther', result: 'L', date: '2023-12-18', event: 'Monday Night Raw' },
    ],
    momentumScore: 8,
    careerStats: {
      totalMatches: 1678,
      wins: 1123,
      losses: 445,
      draws: 110,
      winPercentage: 66.9,
    },
    championships: [
      '2x WWE Champion',
      '1x Universal Champion',
      '2x Intercontinental Champion',
      '5x Tag Team Champion',
      '1x Money in the Bank Winner'
    ],
    bio: 'The Monday Night Messiah and leader of The Authority, Seth Rollins is known for his incredible athleticism and mic skills.'
  },
  {
    id: 'drew-mcintyre',
    name: 'Drew McIntyre',
    nickname: 'The Scottish Warrior',
    realName: 'Andrew McLean Galloway IV',
    image: 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&h=400&fit=crop&crop=face',
    age: 38,
    height: '6\'5"',
    weight: '265 lbs',
    hometown: 'Ayr, Scotland',
    signatureMoves: ['Claymore Kick', 'Future Shock DDT', 'Glasgow Kiss'],
    recentMatches: [
      { id: '1', opponent: 'Cody Rhodes', result: 'L', date: '2024-01-05', event: 'Monday Night Raw' },
      { id: '2', opponent: 'John Cena', result: 'L', date: '2024-01-01', event: 'New Year\'s Revolution' },
      { id: '3', opponent: 'Gunther', result: 'W', date: '2023-12-28', event: 'Monday Night Raw' },
      { id: '4', opponent: 'Damian Priest', result: 'W', date: '2023-12-21', event: 'Monday Night Raw' },
      { id: '5', opponent: 'LA Knight', result: 'W', date: '2023-12-14', event: 'SmackDown' },
    ],
    momentumScore: 9,
    careerStats: {
      totalMatches: 1534,
      wins: 1045,
      losses: 389,
      draws: 100,
      winPercentage: 68.1,
    },
    championships: [
      '2x WWE Champion',
      '1x Intercontinental Champion',
      '1x Tag Team Champion',
      '1x NXT Champion'
    ],
    bio: 'The Scottish Warrior fought his way back to the top of WWE after proving himself around the world.'
  },
  {
    id: 'gunther',
    name: 'Gunther',
    nickname: 'The Ring General',
    realName: 'Walter Hahn',
    image: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&h=400&fit=crop&crop=face',
    age: 36,
    height: '6\'4"',
    weight: '312 lbs',
    hometown: 'Vienna, Austria',
    signatureMoves: ['Powerbomb', 'Big Boot', 'Sleeper Hold'],
    recentMatches: [
      { id: '1', opponent: 'Cody Rhodes', result: 'W', date: '2023-12-28', event: 'Monday Night Raw' },
      { id: '2', opponent: 'Seth Rollins', result: 'W', date: '2023-12-18', event: 'Monday Night Raw' },
      { id: '3', opponent: 'Drew McIntyre', result: 'L', date: '2023-12-28', event: 'Monday Night Raw' },
      { id: '4', opponent: 'LA Knight', result: 'W', date: '2023-12-11', event: 'SmackDown' },
      { id: '5', opponent: 'Ricochet', result: 'W', date: '2023-12-04', event: 'Monday Night Raw' },
    ],
    momentumScore: 12,
    careerStats: {
      totalMatches: 987,
      wins: 723,
      losses: 201,
      draws: 63,
      winPercentage: 73.3,
    },
    championships: [
      '1x Intercontinental Champion (longest reign)',
      '1x NXT UK Champion',
      '1x Tag Team Champion'
    ],
    bio: 'The Ring General dominated NXT UK and brought his no-nonsense style to the main roster with devastating effect.'
  }
];

module.exports = wrestlers; 