# Panda3D Imports
from panda3d.core import loadPrcFileData
from panda3d.core import loadPrcFile
from direct.actor.Actor import Actor
from pandac.PandaModules import *
from direct.task import Task
import math
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import Point3
from pandac.PandaModules import *
from direct.interval.ActorInterval import ActorInterval
from direct.interval.IntervalGlobal import *
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import Vec3, Vec4, BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import os
from direct.gui.DirectGui import *
from direct.gui import DirectGuiGlobals as DGG

loadPrcFileData("", "interpolate-frames 1")


""""""


"""Character customaztion of Big Cheese"""

"""
MAJOR BUGS:
1. (FIXED)Nametag clips thorugh it's background when viewed at an angle
2. (Not a problem in testing)Mouse is locked, and may cause issues w/camera and/or GUI
3. (FIXED)Button textures can't be found error
4. Text Box doesnt change text of other objects
"""

class MyApp(ShowBase):

        def __init__(self):
                ShowBase.__init__(self)
                self.loadModels()
                self.loadCog()
                self.loadCam()
                self.loadGUI()
                self.animations()


        #models
        def loadModels(self):
                self.training = self.loader.loadModel('phase_10\models\cogHQ\MidVault.bam')
                self.training.reparentTo(self.render)

                self.music = self.loader.loadSfx('phase_3/audio/bgm\create_a_toon.ogg')
                self.music.setVolume(.3)
                self.music.play()

                self.desk = self.loader.loadModel('phase_3.5\models\modules\desk_only_wo_phone.bam')
                self.desk.reparentTo(self.render)
                self.desk.setPosHprScale((130, 7.5, 70.75), (120, 0, 0), (1.5, 1.5, 1.5))

                self.chair = self.loader.loadModel('phase_5.5\models\estate\deskChair.bam')
                self.chair.reparentTo(self.render)
                self.chair.setPosHprScale((135, 7, 70.75), (-60, 0, 0), (1.5, 1.5, 1.5))

        #cogs/goons/bosses
        def loadCog(self):
                #cog
                self.Cog = Actor('phase_3.5\models\char\suitA-mod.bam',
                                 {'Flail': 'phase_4\models\char\suitA-flailing.bam',
                                  'Stand': 'phase_4\models\char\suitA-neutral.bam',
                                  'Walk': 'phase_4\models\char\suitA-walk.bam',
                                  'Golf': 'phase_5\models\char\suitA-golf-club-swing.bam',
                                  'Victory' : 'phase_4\models\char\suitA-victory.bam'}
                                 )

                self.Cog.reparentTo(self.render)
                self.CogHead = self.loader.loadModel('phase_4\models\char\suitA-heads.bam').find('**/bigcheese')

                self.CogHead.reparentTo(self.Cog.find('**/joint_head'))
                self.CogHead.setPos(0, 0, -.05)

                self.CogTorso = self.loader.loadTexture('phase_3.5\maps\c_blazer.jpg')
                self.CogTorso2 = self.loader.loadTexture('phase_3.5\maps\l_blazer.jpg')
                self.Cog.find('**/torso').setTexture(self.CogTorso, 1)

                self.Cog.setPosHprScale((130, -12.5, 70.75),(65, 0, 0),(1, 1, 1))

                self.hat1 = self.loader.loadModel('phase_4\models/accessories/tt_m_chr_avt_acc_hat_fez.bam')
                self.hat1.reparentTo(self.CogHead)
                self.hat1.setPosHprScale((0, -0.1, 1.5), (30, -10, 0), (.4, .4, .4))

                self.Cog.loop('Stand')

                self.Cog2 = Actor('phase_3.5\models\char\suitC-mod.bam',
                                  {'Sit' : 'phase_11\models\char\suitC-sit.bam'})

                self.Cog2.reparentTo(self.chair)
                self.Cog2.setPosHprScale((0,-2,0), (180, 0, 0), (.8, .8, .8))
                self.Cog2.loop('Sit')

                self.CogHead2 = self.loader.loadModel('phase_3.5\models\char\suitC-heads.bam').find('**/coldcaller')
                self.CogHead2.reparentTo(self.Cog2.find('**/joint_head'))
                self.CogHead2.setPos(0,0,-.05)

                self.hat2 = self.loader.loadModel('phase_4\models/accessories/tt_m_chr_avt_acc_hat_fedora.bam')
                self.hat2.reparentTo(self.CogHead2)
                self.hat2.setPosHprScale((0, 0, .9),(0, 0, 0),(.5, .5, .5))

                #goon
                self.goon = Actor('phase_9\models\char\Cog_Goonie-zero.bam',\
                                  {'Walk' : 'phase_9\models\char\Cog_Goonie-walk.bam'})
                self.goon.reparentTo(self.render)
                self.goon.setPosHprScale((150, -30, 70.65),(180, 0, 0),(2, 2, 2))

        #animations
        def animations(self):
                stand = self.Cog.actorInterval('Stand', duration=7.5, loop=1)
                victory = self.Cog.actorInterval('Victory', duration=7.5, loop=0)
                scared = self.Cog.actorInterval('Flail', duration=1.5, loop=0)
                walka = self.goon.actorInterval('Walk', duration=6, loop=1)
                walkb = self.goon.actorInterval('Walk', duration=1.5, loop=1)
                sit = self.Cog2.actorInterval('Sit', duration=10, loop=1)

                walk1 = self.goon.posInterval(6, Point3(150, 12.5, 70.65))
                turn1 = self.goon.hprInterval(1.5, Vec3(0,0,0))
                walk2 = self.goon.posInterval(6, Point3(150, -30, 70.65))
                turn2 = self.goon.hprInterval(1.5, Vec3(180, 0, 0))
                spiny = self.hat1.hprInterval(20, Vec3(1000, 0, 0))
                head1 = self.CogHead.hprInterval(2.5, Vec3(30, 10, 0))
                head2 = self.CogHead.hprInterval(2.5, Vec3(0, 0, 0))
                head3 = self.CogHead.hprInterval(2.5, Vec3(-30, 20, 0))
                head4 = self.CogHead.hprInterval(2.5, Vec3(-0, 0, 0))
                head11 = self.CogHead2.hprInterval(2.5, Vec3(15, 10, 0))
                head22 = self.CogHead2.hprInterval(2.5, Vec3(0, 0, 0))
                head33 = self.CogHead2.hprInterval(2.5, Vec3(-15, 10, 5))
                head44 = self.CogHead2.hprInterval(2.5, Vec3(-0, 0, 0))

                #sequences
                #goon
                self.pace = Sequence(
                             Parallel(walka, walk1),
                              Parallel(turn1, walkb),
                                Parallel(walk2, walka),
                                  Parallel(walkb, turn2)
                             )
                self.pace.loop()

                #cog
                self.pace2 = Sequence(
                                stand,
                                Parallel(stand, head1),
                                Parallel(stand, head2),
                                scared,
                                Parallel(stand, head3),
                                Parallel(stand, head4),
                                victory, stand,
                        )
                #second cog
                self.pace2.loop()

                self.pace3 = Sequence(
                        sit,
                        Parallel(sit, head11),
                        Parallel(sit, head22),
                        Parallel(sit, head33),
                        Parallel(sit, head44)
                )
                self.pace3.loop()

        #camera settings
        def loadCam(self):
                self.disable_mouse()
                self.camera.reparentTo(self.render)
                self.camera.setPosHpr((90, 0, 75), (80, 180, -180))

        #GUI settings
        def loadGUI(self):

                #gui files
                self.txtb1 = self.loader.loadModel \
                        ('phase_3\models\props\chatbox.bam')

                self.font1 = self.loader.loadFont('Impress.egg')

                self.click = self.loader.loadSfx('phase_3/audio\sfx\GUI_create_toon_fwd.ogg')
                self.click.setVolume(.75)

                self.rollover = self.loader.loadSfx('phase_3/audio\sfx\GUI_rollover.ogg')
                self.rollover.setVolume(1)

                self.grunt = self.loader.loadSfx('phase_3.5/audio\dial\COG_VO_grunt.ogg')

                self.img1 = self.loader.loadModel('phase_3\models\gui\ChatPanel.bam')

                self.guiimage = self.loader.loadModel('phase_3\models\gui\dialog_box_gui.bam')

                # text for textob1
                #self.text1 = ('Big Cheese', 'Big Cheese', 'Big Cheese', 'Big Cheese')

                # cog tag
                self.textob1 = DirectButton(text='Big Cheese    lvl 12',
                                            text_wordwrap= 5,
                                            parent=self.aspect2d,
                                            pos=(.485, .45, .475),
                                            relief=None,
                                            text_scale=(.05),
                                            hpr=(0, 0, 0),
                                            text_bg=(255, 255, 255, 0.5),
                                            text_font=self.font1,
                                            text_fg=(0, 0, 0, 1),
                                            clickSound=self.grunt,
                                            textMayChange=1,
                                            # command=self.destroygui()
                                            )

                self.textob1.component('text0').textNode.setCardDecal(1)
                self.textob1['text'] = 'Big Cheese    lvl 12'

                #background of textbox
                self.textob2 = DirectLabel(parent=self.Cog,
                                            text= '',
                                            text_wordwrap = 10,
                                            relief=None,
                                            text_scale=1,
                                            pos=(-5, 10, 10),
                                            hpr=(190, 0, 0),
                                            image=self.guiimage,
                                            image_pos=(4.25, .3, -1.25),
                                            image_scale=(4.1, 3, 5.5),
                                            textMayChange=1,
                                            text_font=self.font1)

                self.textob3 = DirectButton(text='Cold Caller           LvL 5',
                                            text_wordwrap=8,
                                            parent=self.aspect2d,
                                            pos=(-1.225, .45, .4),
                                            relief=None,
                                            text_scale=(.05),
                                            hpr=(0, 0, 0),
                                            text_bg=(254, 255, 255, 0.5),
                                            text_font=self.font1,
                                            text_fg=(0, 0, 0, 1),
                                            clickSound=self.grunt,
                                            textMayChange=1,
                                            )



                #textbox
                self.entry = DirectEntry(text='',
                                         scale=.05,
                                         command=self.textob2.setText(),
                                         initialText='You can type here.  It will not affect anything.',
                                         numLines=10,
                                         focus=1,
                                         focusInCommand=self.textob2.clearText(),
                                         parent=self.aspect2d,
                                         pos=(1.45, .1, .8),
                                         entryFont=self.font1,
                                         relief=None,
                                         clickSound=self.click,
                                         rolloverSound=self.rollover,
                                         text_align=TextNode.ACenter
                                         )


                #main panel
                self.guipanel = DirectLabel(parent=self.Cog,
                                            text= 'Click the arrows to pick your options.',
                                            text_wordwrap = 10,
                                            relief=None,
                                            text_scale=.5,
                                            pos=(8, 10, 8),
                                            hpr=(200, 0, 0),
                                            image=self.guiimage,
                                            image_pos=(2, .3 , -1.25),
                                            image_scale=(10, 5, 5),
                                            textMayChange=1,
                                            text_font=self.font1)


                #gui buttons
                self.b1 = DirectButton(text=('Next', 'Loading...', 'Go to Next', ''),
                                      text_scale=.05,
                                      text_font=self.font1,
                                      text_pos=(-.05, .125, 1),
                                      pressEffect=1,
                                      geom_scale=(1, 6, 1),
                                      relief=None,
                                      frameColor=(255, 0, 0, 0.8),
                                      clickSound=self.click,
                                      rolloverSound=self.rollover,
                                      textMayChange=1,
                                      image=self.img1,
                                      image_scale=(.25, .09, .09),
                                      image_pos=(-.175, .2, .19),
                                      #command=self.changeAnim()
                                      )


                self.b2 = DirectButton(text=('Back', 'Loading...', 'Go Back', ''),
                                       text_scale=.05,
                                       text_font=self.font1,
                                       text_pos=(-.55, .125, 1),
                                       pressEffect=1,
                                       geom_scale=(1, 6, 1),
                                       relief=None,
                                       frameColor=(255, 0, 0, 0.8),
                                       clickSound=self.click,
                                       rolloverSound=self.rollover,
                                       image=self.img1,
                                       image_scale=(.25, .09, .09),
                                       image_pos=(-.675, .2, .19),
                                       textMayChange=1,
                                       )

        def setText(self, textEntered):
                self.textob2.setText(textEntered)

        def clearText(self):
                self.entry.enterText('')

        #def changeAnim(self):
                        #self.Cog.stop('Stand')


        #def changeHat(self):
                        #self.hat1.removeNode(),
                        #self.hat2.reparentTo(self.CogHead)
                        #self.hat2.setPosHprScale((0, 0, 1.5), (30, -10, 0), (.25, .25, .25))

        #def destroygui(self):
                #self.textob2.destroy()

app = MyApp()
app.run()