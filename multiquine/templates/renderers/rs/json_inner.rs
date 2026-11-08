// LDA_REQUIRES: json
    renderers.insert("json_inner", |s| { let q = json(s); q[1..q.len()-1].to_owned() });
