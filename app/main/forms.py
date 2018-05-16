from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, DataRequired, Length, Email, Regexp, ValidationError

from app.models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(1,64)])
    location = StringField('地址', validators=[Length(1,64)])
    about_me = TextAreaField('自我简介')
    submit = SubmitField('编辑')

class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
               '用户名名必须为字母、数字或下滑线')])
    confirmed = BooleanField('激活')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(1,64)])
    location = StringField('地址', validators=[Length(1,64)])
    about_me = TextAreaField('自我简介')
    submit = SubmitField('编辑')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册，直接登录或更换邮箱')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')
# blog 文章表单
class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1,64)])
    body = PageDownField('内容', validators=[DataRequired()])
    tag = StringField('标签', validators=[DataRequired(), Length(1,10)])
    submit = SubmitField('保存')

class CommentForm(FlaskForm):
    body = PageDownField('', validators=[DataRequired()])
    submit = SubmitField('回复')