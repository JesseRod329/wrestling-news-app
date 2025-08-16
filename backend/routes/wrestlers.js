const express = require('express');
const router = express.Router();
const supabase = require('../supabaseClient');

router.get('/', async (req, res) => {
  let query = supabase.from('wrestlers').select('*');

  if (req.query.search) {
    query = query.ilike('name', `%${req.query.search}%`);
  }

  const { data: wrestlers, error } = await query;

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  const processedWrestlers = wrestlers.map(wrestler => {
    let wins = 0;
    let losses = 0;
    if (wrestler.recent_matches) {
      wrestler.recent_matches.forEach(match => {
        if (match.result === "Win") wins++;
        if (match.result === "Loss") losses++;
      });
    }
    return {
      ...wrestler,
      careerStats: {
        wins,
        losses,
        draws: 0 // Assuming draws are not tracked in this data
      }
    };
  });

  res.json(processedWrestlers);
});

router.get('/:id', async (req, res) => {
  const { data: wrestler, error } = await supabase
    .from('wrestlers')
    .select('*')
    .eq('id', req.params.id)
    .single();

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  if (!wrestler) {
    return res.status(404).json({ error: 'Wrestler not found' });
  }
  
  let wins = 0;
  let losses = 0;
  if (wrestler.recent_matches) {
    wrestler.recent_matches.forEach(match => {
      if (match.result === "Win") wins++;
      if (match.result === "Loss") losses++;
    });
  }

  res.json({
    ...wrestler,
    careerStats: {
      wins,
      losses,
      draws: 0 // Assuming draws are not tracked in this data
    }
  });
});

module.exports = router; 