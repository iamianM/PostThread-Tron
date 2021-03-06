import { CONSTANTS } from '../../../../constants/Constants';

// http://localhost:3000/api/user/interact/follow?user_msa_id=1&user_msa_id_to_interact_with=2
// http://localhost:3000/api/user/interact/unfollow?user_msa_id=1&user_msa_id_to_interact_with=2

export default async function handler(req, res) {
    if (req.method === 'POST') {
        const query = req.query;
        const method = query.method
        const data = await fetch(`${CONSTANTS.server}/user/interact/${method}?` + new URLSearchParams({
            ...req.query
        }), {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        return res.status(200).json(await data.json())
    }
}