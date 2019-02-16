from flask import Blueprint, request, jsonify
from app.db import Absence, qtAbsence, Subjectur, User
from flask_jwt_extended import ( jwt_required, get_jwt_identity )

abapp = Blueprint('rabsence',__name__)

#not used
@abapp.route('/one/<int:subjid>', methods=['GET'])
@jwt_required
def getabsences(subjid):
    userid = get_jwt_identity()
    qtaulas = qtAbsence.query.filter_by(subject_id=subjid).count()
    qtdispo = Absence.query.filter_by(subject_id=subjid,user_id=userid).count()
    data = {'subjid':subjid,
            'presencas':qtdispo,
            'faltas':qtaulas-qtdispo }
    return jsonify(data), 200


@abapp.route('/all/<int:subjid>', methods=['GET'])
@jwt_required
def getallabsences(subjid):
    subjectur = Subjectur.query.filter_by(subj_id=subjid)
    if subjectur == None:
        return jsonify({'Error':'Nenhum discente relacionado a disciplina foi encontrado'}), 404
    qtaulas = qtAbsence.query.filter_by(subject_id=subjid).count()
    data = []
    for sur in subjectur:
        dic = {}
        qtdispo = Absence.query.filter_by(subject_id=subjid, user_id=sur.user_id)
        user = User.query.filter_by(id=sur.user_id).first()
        dic['username'] = f'{user.username} - {user.enrolment}'
        dic['dates'] = [row.date.strftime("%Y-%m-%d") for row in qtdispo]
        dic['presencas'] = qtdispo.count() 
        dic['faltas'] = qtaulas - qtdispo.count()
        data.append(dic)
    return jsonify({'values':data}), 200    
